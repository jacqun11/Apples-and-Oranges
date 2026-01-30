"""
FastAPI backend for AI-powered creative evaluation platform.
Main entry point with /query endpoint.
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import PyPDF2
import io

from schemas import QueryResponse
from orchestrator import route

# Default rubric text (used when no rubric file is provided)
DEFAULT_RUBRIC = """SaiL merges arts, technology, and social impact to unite and inspire humanity through entertaining and transformative storytelling.

In an era characterized by a fragmented and often polarizing media landscape, the studio operates on a central, guiding principle: the cultivation of Actionable Hope. This goes beyond passive inspiration and focuses on empowering audiences with clarity and motivation to create change.

Each project functions as the epicenter of a potential movement. Stories are developed alongside strategies for real-world engagement—such as partnerships, community resources, or platforms for dialogue—transforming audiences from passive viewers into active participants.

Evaluation Questions:
- Does the story have a positive message?
- Does the story uplift and inspire?
- Does the story align with the Heroine's Journey?
- Does the story address a critical problem worth solving?
- Is there potential for measurable impact?
- Is the story commercially viable? (not a deciding factor alone)
- Do the author(s) align with the studio's mission?"""

app = FastAPI(
    title="Creative Evaluation Platform",
    description="AI-powered platform for evaluating creative scripts and content",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text content from a PDF file.
    
    Args:
        file_content: Binary content of the PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """
    Extracts text content from a TXT file.
    
    Args:
        file_content: Binary content of the TXT file
        
    Returns:
        Extracted text as string
    """
    try:
        # Try UTF-8 first, fallback to latin-1
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        return file_content.decode('latin-1')


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Creative Evaluation Platform API", "status": "running"}


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    text_input: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    script_file: Optional[UploadFile] = File(None),
    rubric_file: Optional[UploadFile] = File(None)
):
    """
    Main query endpoint that accepts text input, script file upload, rubric file upload, and optional prompt.
    
    Accepts:
    - text_input: Optional text string (script content)
    - prompt: Optional prompt/instruction string (renamed from question)
    - script_file: Optional script file upload (PDF or TXT)
    - rubric_file: Optional rubric/values file upload (PDF or TXT)
    
    Returns:
    - Structured JSON response with agent evaluation results
    """
    # Collect script content from all sources
    content_parts = []
    
    # Add text input if provided
    if text_input:
        content_parts.append(text_input.strip())
    
    # Process script file if provided
    if script_file:
        file_content = await script_file.read()
        file_extension = script_file.filename.split('.')[-1].lower() if script_file.filename else ''
        
        if file_extension == 'pdf':
            extracted_text = extract_text_from_pdf(file_content)
            content_parts.append(extracted_text)
        elif file_extension == 'txt':
            extracted_text = extract_text_from_txt(file_content)
            content_parts.append(extracted_text)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}. Only PDF and TXT are supported."
            )
    
    # Combine all script content
    content_text = "\n\n".join(content_parts)
    
    # Validate that we have some script content
    if not content_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No script content provided. Please provide text_input or upload a script_file."
        )
    
    # Process rubric file if provided, otherwise use default
    rubric_text = DEFAULT_RUBRIC  # Default fallback
    
    if rubric_file:
        # User provided a rubric file, extract its content
        file_content = await rubric_file.read()
        file_extension = rubric_file.filename.split('.')[-1].lower() if rubric_file.filename else ''
        
        if file_extension == 'pdf':
            rubric_text = extract_text_from_pdf(file_content)
        elif file_extension == 'txt':
            rubric_text = extract_text_from_txt(file_content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported rubric file type: {file_extension}. Only PDF and TXT are supported."
            )
    
    # Route to orchestrator with content_text, prompt, and rubric_text
    try:
        result = route(content_text, prompt, rubric_text)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


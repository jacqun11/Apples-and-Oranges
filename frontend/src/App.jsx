import React, { useState } from 'react'
import './App.css'

function App() {
  const [textInput, setTextInput] = useState('')
  const [prompt, setPrompt] = useState('')
  const [scriptFile, setScriptFile] = useState(null)
  const [rubricFile, setRubricFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentResult, setCurrentResult] = useState(null)
  const [history, setHistory] = useState([])

  const handleScriptFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Validate file type
      const fileExtension = selectedFile.name.split('.').pop().toLowerCase()
      if (fileExtension !== 'pdf' && fileExtension !== 'txt') {
        setError('Only PDF and TXT files are supported.')
        setScriptFile(null)
        return
      }
      setScriptFile(selectedFile)
      setError(null)
    }
  }

  const handleRubricFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Validate file type
      const fileExtension = selectedFile.name.split('.').pop().toLowerCase()
      if (fileExtension !== 'pdf' && fileExtension !== 'txt') {
        setError('Only PDF and TXT files are supported.')
        setRubricFile(null)
        return
      }
      setRubricFile(selectedFile)
      setError(null)
    }
  }

  // Auto-resize prompt textarea (chat-style)
  const handlePromptChange = (e) => {
    setPrompt(e.target.value)
    // Auto-resize textarea
    const textarea = e.target
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px' // Max height 200px
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validate input
    if (!textInput.trim() && !scriptFile) {
      setError('Please provide text input or upload a script file.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Create FormData for multipart/form-data
      const formData = new FormData()
      
      if (textInput.trim()) {
        formData.append('text_input', textInput.trim())
      }
      
      if (prompt.trim()) {
        formData.append('prompt', prompt.trim())
      }
      
      if (scriptFile) {
        formData.append('script_file', scriptFile)
      }
      
      if (rubricFile) {
        formData.append('rubric_file', rubricFile)
      }

      // Send request to backend
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to process query')
      }

      const result = await response.json()
      
      // Update current result
      setCurrentResult(result)
      
      // Add to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        agent: result.agent_used,
        summary: result.summary,
        score: result.score,
      }
      setHistory(prev => [historyItem, ...prev])
      
      // Clear form
      setTextInput('')
      setPrompt('')
      setScriptFile(null)
      setRubricFile(null)
      // Reset file inputs
      const fileInputs = document.querySelectorAll('input[type="file"]')
      fileInputs.forEach(input => input.value = '')
      // Reset prompt textarea height
      const promptTextarea = document.getElementById('prompt-input')
      if (promptTextarea) {
        promptTextarea.style.height = 'auto'
      }
      
    } catch (err) {
      setError(err.message || 'An error occurred while processing your query.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 0.7) return '#27ae60' // Green
    if (score >= 0.5) return '#f39c12' // Orange
    return '#e74c3c' // Red
  }

  return (
    <div className="app">
      {/* Header Section */}
      <header className="header">
        <h1>Creative Evaluation Platform</h1>
        <p>AI-powered evaluation for creative scripts and content</p>
      </header>

      {/* Input Section */}
      <section className="input-section">
        <h2>Submit Content for Evaluation</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="text-input">Paste script or notes here</label>
            <textarea
              id="text-input"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Enter your script, notes, or content here..."
              disabled={loading}
              className="script-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="script-file-input">Upload Script File (PDF or TXT)</label>
            <input
              id="script-file-input"
              type="file"
              accept=".pdf,.txt"
              onChange={handleScriptFileChange}
              disabled={loading}
            />
            {scriptFile && (
              <div className="file-info">
                Selected: {scriptFile.name} ({(scriptFile.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>

          <div className="form-group rubric-group">
            <label htmlFor="rubric-file-input">Evaluation Rubric / Studio Values (Optional)</label>
            <input
              id="rubric-file-input"
              type="file"
              accept=".pdf,.txt"
              onChange={handleRubricFileChange}
              disabled={loading}
            />
            <div className="helper-text">
              Upload a document describing the values or rubric to evaluate against. If none is provided, a general studio rubric will be used.
            </div>
            {rubricFile && (
              <div className="file-info">
                Selected: {rubricFile.name} ({(rubricFile.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="prompt-input">Prompt</label>
            <textarea
              id="prompt-input"
              value={prompt}
              onChange={handlePromptChange}
              placeholder="Ask a question or give instructions (e.g., 'Evaluate impact and risks')"
              disabled={loading}
              className="prompt-input"
              rows="1"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="submit-button"
            disabled={loading || (!textInput.trim() && !scriptFile)}
          >
            {loading ? 'Processing...' : 'Submit for Evaluation'}
          </button>
        </form>
      </section>

      {/* Agent Output Section */}
      <section className="output-section">
        <h2>Evaluation Results</h2>
        {loading ? (
          <div className="loading">Processing your query...</div>
        ) : currentResult ? (
          <div className="output-content">
            <div className={`agent-badge ${currentResult.agent_used === 'impact_agent' ? 'impact' : ''}`}>
              {currentResult.agent_used === 'impact_agent' ? 'Impact Agent' : 'Script Reviewer'}
            </div>
            
            <div className="summary">{currentResult.summary}</div>
            
            <div className="score-container">
              <div className="score-label">
                <span>Evaluation Score</span>
                <span className="score-value">{(currentResult.score * 100).toFixed(0)}%</span>
              </div>
              <div className="score-bar-container">
                <div
                  className="score-bar"
                  style={{
                    width: `${currentResult.score * 100}%`,
                    backgroundColor: getScoreColor(currentResult.score)
                  }}
                >
                  {(currentResult.score * 100).toFixed(0)}%
                </div>
              </div>
            </div>

            <div className="details">
              <h3>Detailed Analysis</h3>
              {Object.entries(currentResult.details).map(([key, value]) => {
                // Skip evaluation_notes in display (or show it if you want)
                if (key === 'evaluation_notes') return null
                
                // Handle array values
                const displayValue = Array.isArray(value) 
                  ? value.join(', ') 
                  : value
                
                return (
                  <div key={key} className="detail-item">
                    <span className="detail-label">
                      {key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ')}:
                    </span>
                    <span className="detail-value">{displayValue}</span>
                  </div>
                )
              })}
            </div>
          </div>
        ) : (
          <div className="no-output">No evaluation results yet. Submit content above to get started.</div>
        )}
      </section>

      {/* Interaction History Section */}
      <section className="history-section">
        <h2>Interaction History</h2>
        {history.length > 0 ? (
          <ul className="history-list">
            {history.map((item) => (
              <li key={item.id} className="history-item">
                <div className="history-header">
                  <span className="history-timestamp">{item.timestamp}</span>
                  <span className={`history-agent ${item.agent === 'impact_agent' ? 'impact' : ''}`}>
                    {item.agent === 'impact_agent' ? 'Impact Agent' : 'Script Reviewer'}
                  </span>
                </div>
                <div className="history-summary">
                  Score: {(item.score * 100).toFixed(0)}% - {item.summary}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="no-history">No interaction history yet.</div>
        )}
      </section>
    </div>
  )
}

export default App


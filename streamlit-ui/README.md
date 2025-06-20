# 🤖 Agno Knowledge Base Playground

An interactive web application that allows you to create AI agents with knowledge from any website using the Agno framework.

## Features

- 🌐 **URL Input**: Enter any website URL to create a knowledge base
- 🔧 **Configurable Settings**: Adjust crawling depth, model selection, and collection names
- 💬 **Interactive Chat**: Chat with your AI agent about the website content
- 📊 **Real-time Status**: See the progress of knowledge base loading
- 🎨 **Modern UI**: Clean, intuitive interface built with Streamlit

## Prerequisites

Before running the playground, make sure you have:

1. **Python 3.8+** installed
2. **MongoDB** running (local or cloud)
3. **Ollama** installed and running with at least one model
4. **Internet connection** for website crawling

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables

Create a `.env` file in the project root:

```env
mdb_url=mongodb://localhost:27017
```

Replace with your MongoDB connection string if using a cloud database.

### 3. Install Ollama Models

Make sure you have at least one of these models installed in Ollama:

```bash
# Install a model (choose one)
ollama pull llama3.1
ollama pull llama3.2
ollama pull openhermes
ollama pull mistral
```

### 4. Start Ollama

```bash
ollama serve
```

## Usage

### Running the Playground

```bash
streamlit run agno_playground.py
```

The playground will open in your browser at `http://localhost:8501`.

### How to Use

1. **Enter a URL** in the sidebar - this will be the website the agent learns from
2. **Configure settings**:
   - Maximum links to crawl (1-50)
   - Ollama model selection
   - Knowledge base collection name
3. **Click "Initialize Agent"** to start the knowledge base loading process
4. **Start chatting** with your agent about the website content!

### Example URLs to Try

- Documentation sites: `https://docs.agno.com/introduction`
- News websites: `https://example-news-site.com`
- Educational content: `https://example-educational-site.com`
- Company websites: `https://example-company.com`

## Configuration Options

### Model Selection
- **llama3.1**: Good balance of performance and speed
- **llama3.2**: Latest Llama model with improved capabilities
- **llama3.2-vision**: Supports image analysis (if needed)
- **openhermes**: Optimized for instruction following
- **mistral**: Fast and efficient model

### Crawling Settings
- **Max Links**: Controls how many pages from the website to crawl
- **Collection Name**: Custom name for the MongoDB collection storing the knowledge

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check your connection string in `.env`
   - Verify network connectivity

2. **Ollama Model Not Found**
   - Install the required model: `ollama pull <model_name>`
   - Ensure Ollama is running: `ollama serve`

3. **Website Crawling Issues**
   - Some websites may block automated crawling
   - Try different URLs or reduce max links
   - Check internet connectivity

4. **Memory Issues**
   - Reduce max links for large websites
   - Use a smaller model
   - Ensure sufficient system memory

### Error Messages

- **"Error initializing agent"**: Check MongoDB and Ollama setup
- **"Model not found"**: Install the selected Ollama model
- **"Connection timeout"**: Verify network and service availability

## Architecture

The playground uses:

- **Agno**: AI agent framework for knowledge management and reasoning
- **Streamlit**: Web interface for user interaction
- **MongoDB**: Vector database for storing embeddings
- **Ollama**: Local LLM inference
- **WebsiteKnowledgeBase**: Web crawling and content extraction

## Contributing

Feel free to contribute to this project by:

1. Reporting bugs
2. Suggesting new features
3. Improving documentation
4. Adding new model integrations

## License

This project is open source and available under the MIT License.

## Resources

- [Agno Documentation](https://docs.agno.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Ollama Documentation](https://ollama.ai/docs)
- [MongoDB Documentation](https://docs.mongodb.com)
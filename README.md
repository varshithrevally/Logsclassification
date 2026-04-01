## Logs Classification With Hybrid Classification Framework

This project implements a hybrid log classification system designed to handle log data with varying levels of complexity and structure. Instead of relying on a single technique, it combines rule-based, machine learning, and LLM-based approaches to achieve more reliable and adaptable classification across different types of log patterns.

The system is built to work efficiently with both well-structured logs and ambiguous or poorly labeled data. By selecting the appropriate classification strategy based on the nature of the input, it ensures better accuracy and flexibility in real-world scenarios.

## Overview

Log data often ranges from highly predictable patterns to completely unstructured messages. A single model is rarely sufficient to handle this diversity. This project addresses that limitation by integrating three complementary classification methods:

- Regex-based classification for simple and deterministic patterns
- Sentence Transformer embeddings with Logistic Regression for learned patterns
- LLM-based classification for edge cases and low-data scenarios

These methods work together to form a layered classification pipeline.

## Classification Approaches

1. Regular Expression (Regex)

- Handles simple and predictable log patterns
- Works well when log formats are consistent
- Uses predefined rules for classification
- Very fast and lightweight compared to other methods
- Used as the first layer in the classification pipeline

2. Sentence Transformer + Logistic Regression

- Designed for moderately complex log patterns
- Requires sufficient labeled training data
- Converts log messages into dense vector embeddings
- Uses Logistic Regression for final classification
- Captures semantic meaning beyond exact text matching
- Provides a balance between accuracy and performance

3. Large Language Models (LLM)

- Used for highly complex or ambiguous log patterns
- Does not require large labeled datasets
- Acts as a fallback when other methods fail or have low confidence
- Understands context and intent in log messages
- Effective for handling unseen or rare log formats
- Improves overall robustness of the system

## Architecture

<img width="922" height="584" alt="architecture" src="https://github.com/user-attachments/assets/57636893-ce27-421d-ad80-1a6afc56abe1" />
The system follows a hybrid decision flow:

1. Attempt classification using regex rules
2. If no match is found, use the trained ML model
3. If confidence is low or the pattern is ambiguous, fall back to LLM

This layered approach ensures both efficiency and coverage across different types of log data.

## **Folder Structure**

```
Log Classification/
├── models/
│   └── logclassifier.joblib
├── resources/
│   ├── test.csv
│   └── output.csv
├── templates/
│   └── index.html
├── training/
│   └── synthetic_logs.csv
├── server.py
├── classify.py
├── processor_bert.py
├── processor_llm.py
├── processor_regex.py
└── requirements.txt
```

- training/: Contains scripts for training the Sentence Transformer embeddings and Logistic Regression model, along with regex-based classification logic
- models/: Stores trained models and embeddings used during inference
- resources/: Includes sample datasets, outputs, and supporting files
- templates/: Contains frontend files, including the main index.html for interacting with the API
- server.py: FastAPI application that exposes endpoints for log classification

## Setup Instructions

1. Install Dependencies
   Ensure Python is installed, then install the required libraries:

```
pip install -r requirements.txt
```

3. Run the FastAPI Server

```
uvicorn server:app --reload
```

## API Access

Once the server is running, the application can be accessed at:

- Main endpoint: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Usage

The system accepts a CSV file containing log entries. The input file must include the following columns:

- source
- log_message

After processing, the system returns a CSV file with an additional column:

- target_label — the predicted classification label for each log entry

## Notes

This project is intended for scenarios where log data varies significantly in structure and quality. The hybrid design allows it to scale from simple rule-based classification to more advanced contextual understanding without requiring a complete redesign of the system.

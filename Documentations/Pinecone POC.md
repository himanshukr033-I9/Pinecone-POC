# POC 1: Pinecone Integrated Embedding & Reranking Features
**Date:** 29th January 2025

## Overview

This proof-of-concept (POC) explores Pinecone's integrated embedding capabilities using a built-in model. The experiments focused on:
- Ingestion of JSON and Markdown files
- Querying data from Pinecone
- Evaluating retrieval performance
- Exploring Pinecone's inbuilt reranking functionality

## Embedding Models

Pinecone offers several embedding models. For this POC, the following models were available:
- **multilingual-e5-large** (used to start the POC)
- **pinecone-sparse-english-v0**

## Data Ingestion Process

### Files Processed
- **JSON Files:** Structured data previously used in BedRock.
- **Markdown Files:** Documentation files.

### Ingestion Details
- **Initial Ingestion:** Both JSON and Markdown files were ingested without chunking.
- **Chunking Attempt:** Manual chunking was attempted for JSON data; however, it did not yield better retrieval performance.

## Key Learnings

- **Pinecone Embedding Feature:** Gained a clear understanding of Pinecone and its embedded model functionalities.
- **File Format Performance:**
  - **Markdown:** Returned correct files for queries.
  - **JSON:** Initially retrieved files that were not related to the query or the associated organization.
- **Ingestion Observations:**
  - Documents are ingested as single chunks by default.
  - Manual chunking for JSON slightly increased the retrieval score (around 0.8) but did not improve result accuracy.

## Reranking Feature

Pinecone includes an inbuilt reranking feature. During this POC:
- Explored the reranking functionality for retrieved results.
- Identified three available reranking models:
  - **Model 1:** 500-token limit (available in the free version)
  - **Model 2:** 1024-token limit (available in the free version)
  - **Model 3:** 40,000-token limit (not accessible in the free version)
- **Note:** Ingesting the entire document as a single chunk causes token counts to exceed the limits of Models 1 and 2.

## Metadata and Category Addition

- **Initial Attempt:** Adding metadata during ingestion resulted in unresolved errors.
- **Workaround:** A "category" field was added with the organization name as its value. This adjustment made JSON query results relate to the organization, but the results did not always align with the specific query intent.

## Results & Outcomes

- **JSON Files:** 
  - Retrieval score around *0.85*
  - Results were not related to the query and organization
- **Markdown Files:** 
  - Retrieval score around *0.82*
  - Results were more relevant to the organization mentioned in the query

## Summary

Today's progress involved understanding and implementing Pinecone's integrated embedding and reranking features. While there were successes (e.g., extracting relevant results for Markdown files), key challenges remain—particularly with JSON file ingestion, metadata handling, and token limit issues for reranking models. Future work will focus on refining chunking strategies and enhancing metadata integration for improved retrieval accuracy.

**Date:** 05 February 2025

## RAG Exploration and Annotation

Started learning RAG from scratch in depth.

- **Annotates RAG Architecture Idea:**  
  We have 3 different types of data structures so we should maintain 3 distinct RAG pipelines. Each pipeline will use different embedding, chunking, and retrieval strategies based on the respective data.
  
- **Chunking Strategies:**  
  - Straightforward chunking after 1000 characters is not optimal.  
  - For Markdown, instead of fixed character limits, chunking should be done based on semantic sections using hierarchical tags (e.g., `##` or `###`) to preserve the meaning and context.
  
- **Observations:**  
  - RAG works best on Markdown as it preserves structure; JSON tends to take more tokens and is less suitable. (https://community.openai.com/t/markdown-is-15-more-token-efficient-than-json/841742)
  - Properly structured Markdown with clear headings improves chunking and context preservation.
  
- **Implementation:**  
  - Wrote new code to convert structured JSON into a better Markdown format.
  - Improved Markdown structure for JSON by incorporating appropriate heading levels.
  
**Conversion Results:**  
  
- **Query:** "What is the mission of the Reach out and Read"  
  - Previous MD score: 0.805  
  - New MD Score: 0.828
  
- **Query:** "Who are the leaders in 2021 for Ceres?"  
  - Previous MD score: 0.805  
  - New MD Score: 0.828
  
- **Query:** "What is the mission of the Reach out and Read"  
  - Previous MD score: 0.8477  
  - New MD Score: 0.824
  
- **Query:** "What are the key activities of American Indian College Fund?"  
  - Previous MD score: 0.8206  
  - New MD Score: 0.823
  
- **Query:** "What is the revenue breakdown for 2022 for Forest Trends Association?"  
  - Previous MD score: 0.8393  
  - New MD Score: 0.832928
 
Next steps: Tomorrow, I will experiment with other chunking methods to evaluate any additional improvements in the retrieval scores.








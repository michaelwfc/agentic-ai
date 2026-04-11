import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

from IPython.display import display, Image, IFrame, Markdown, JSON 

import helper

# OpenAI & ChromaDB - Embedding + Vector Store
import openai
import chromadb

# Langchain 
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class DocumentRAG:
    pass



    def _load_file(self):
      # Load the existing JSON chunks
      with open(ADE_JSON_PATH, "r", encoding="utf-8") as f:
          loaded_chunks = json.load(f)

      print(f"Loaded {len(loaded_chunks)} saved chunks.")

      # Show first chunk structure
      print(f"\n Sample chunk structure:")
      print(json.dumps(loaded_chunks[0], indent=2)[:400] + "...")

      print("\n Ready to query!")
      return loaded_chunks


    def build_vector_db(self):
      loaded_chunks =  self._load_file()
      # Setting Directory and Collectioon name
      CHROMA_DB_PATH = Path("./chroma_db")
      COLLECTION_NAME = "ade_documents"

      # embeding model for vector database 
      EMBEDDING_MODEL = "text-embedding-3-small"

      # Instantiate the Chroma Client
      chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

      # Create or Load ADE Collection
      collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
      print(f"Checking for existing chunks in Chroma...")

      # Get all existing chunk IDs from the collection
      existing_result = collection.get(
                          ids=[chunk["chunk_id"] for chunk in loaded_chunks])
      existing_ids = set(existing_result.get('ids', []))
      print(f"Found {len(existing_ids)} existing chunks in collection")




    def insert_new_chunks(loaded_chunks):
        print(f"Inserting new chunks into Chroma...")

        added_count = 0
        for i, chunk in enumerate(loaded_chunks):
            chunk_id = chunk["chunk_id"]
            
            # Add chunk if it does not exist
            if chunk_id not in existing_ids:
                text = chunk.get("text", "")
                
                # Skip empty chunks
                if not text or not text.strip():
                    continue

                # Generate Embeddings for chunk text with OpenAI
                emb = openai.embeddings.create(
                    input=text,
                    model=EMBEDDING_MODEL
                ).data[0].embedding
                
                # Flatten Metadata (Simple Types Only)
                metadata = {
                    "chunk_type": chunk.get("chunk_type", "unknown"),
                    "page": chunk.get("page", 0)
                }
                
                # Add bbox coordinates to metadata
                bbox = chunk.get("bbox")
                if bbox and len(bbox) == 4:
                    metadata["bbox_x0"] = float(bbox[0])
                    metadata["bbox_y0"] = float(bbox[1])
                    metadata["bbox_x1"] = float(bbox[2])
                    metadata["bbox_y1"] = float(bbox[3])
                
                # Store in Chroma
                collection.add(
                    documents=[text],
                    ids=[chunk_id],
                    metadatas=[metadata],
                    embeddings=[emb]
                )
                
                added_count += 1
                
                # Progress indicator
                if (added_count) % 20 == 0:
                    print(f"   Processed {added_count} new chunks...")

        print(f"\n✓ Added {added_count} new chunks, skipped existing chunks")

    def rag_query(self, question, top_k=3, threshold=0.25, show_images=True):
        """
        Query the ADE Chroma index with a natural language question.
        Dynamically extracts and displays JUST the relevant chunk from 
        the PDF.
        
        Args:
            question (str): User query
            top_k (int): Max results to return
            threshold (float): Minimum similarity (1 - distance)
            show_images (bool): Display chunk-level grounding visualizations
        """
        # 1. Embed Query
        q_embed = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=question
        ).data[0].embedding

        # 2. Query Chroma
        results = collection.query(
            query_embeddings=[q_embed],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        print(f"\n Query: {question}\n")
        print("=" * 80)

        # 3. Parse Results
        retrieved_docs = results["documents"][0]
        retrieved_meta = results["metadatas"][0]
        retrieved_dists = results["distances"][0]
        retrieved_ids = results["ids"][0]

        found_any = False
        for i, (text, meta, dist, cid) in enumerate(zip(
            retrieved_docs, retrieved_meta, retrieved_dists, retrieved_ids
        )):
            similarity = 1 - dist
            # Skip Weak Matches
            if similarity >= threshold:
                
                found_any = True
                page_num = meta.get('page', 0)
                chunk_type = meta.get('chunk_type', 'unknown')
                
                print(f"\n  Result {i+1} (similarity={similarity:.3f}):")
                print(f"   Chunk ID: {cid}")
                print(f"   Type: {chunk_type}, Page: {page_num}" )
                print(f"   Text preview: {text[:200]}...")
                
                # Display chunk-level grounding image
                if show_images:
                    # Extract bbox from metadata if available
                    bbox = None
                    if all(k in meta for k in ['bbox_x0', 'bbox_y0', 'bbox_x1', 'bbox_y1']):
                        bbox = [
                            meta['bbox_x0'],
                            meta['bbox_y0'],
                            meta['bbox_x1'],
                            meta['bbox_y1']
                        ]
                    
                    # Dynamically extract chunk image from PDF
                    print(f"\n Dynamically extracting chunk from PDF...")
                    chunk_img = helper.extract_chunk_image(
                        pdf_path=DOC_PATH,
                        page_num=page_num,
                        bbox=bbox,
                        highlight=True,
                        padding=10
                    )
                    
                    if chunk_img:
                        print(f"{chunk_type.title()} chunk (cropped):")
                        display(Image(data=chunk_img))
                    else:
                        print(f"Could not extract chunk image")
              
            
            print("-" * 80)

        if not found_any:
            print("No results above similarity threshold.")
        
        return results


    print("RAG query function defined with dynamic chunk extraction")


    def search_with_metadata_filter(self,):
        q_embed = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input="What was Apple’s total revenue in 2023?",
        ).data[0].embedding

        results = collection.query(
            query_embeddings=[q_embed],
            n_results=5,
            include=["documents", "metadatas", "distances"],
            where = {"chunk_type": "table"},
        )

        results["documents"]


    def build_retriever(self,):
        vectordb = Chroma(
          collection_name=COLLECTION_NAME,
          embedding_function=OpenAIEmbeddings(model = EMBEDDING_MODEL),
          persist_directory=str(CHROMA_DB_PATH)
        )

        retriever = vectordb.as_retriever()


        # Define prompt template
        system_prompt = (
            "Use the following pieces of retrieved context to answer the "
            "user's question. "
            "If you don't know the answer, say that you don't know."
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # Initialize LLM
        llm = ChatOpenAI(model="gpt-5-mini", temperature = 1)

        # Create the RAG chain
        rag_chain = create_retrieval_chain(retriever, prompt | llm)

        # Invoke the chain (conceptual)
        response = rag_chain.invoke({"input": 
                                    "What were Apple net sales in 2023"})
        print(response["answer"])



        # Invoke the chain (conceptual)
        response = rag_chain.invoke({
            "input": "How did total revenue trend between 2023 and 2022" 
                                              "for iPhone sales?"})
        print(response["answer"])


import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="C:/code2/my_portfolioo.csv"):  # use forward slashes or raw string
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["skills"]],
                    metadatas={"portfolio": row["portfolio"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

from typing import List
import arxiv
import json
import os

PAPER_DIR = "papers"

class MCPServer:
    def search_papers(self, topic: str, max_results: int = 5) -> List[str]:
        client = arxiv.Client()
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        papers = client.results(search)
        path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, "papers_info.json")
        try:
            with open(file_path, "r") as json_file:
                papers_info = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            papers_info = {}
        paper_ids = []
        for paper in papers:
            paper_ids.append(paper.get_short_id())
            paper_info = {
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'summary': paper.summary,
                'pdf_url': paper.pdf_url,
                'published': str(paper.published.date())
            }
            papers_info[paper.get_short_id()] = paper_info
        with open(file_path, "w") as json_file:
            json.dump(papers_info, json_file, indent=2)
        print(f"Results are saved in: {file_path}")
        return paper_ids

    def extract_info(self, paper_id: str) -> str:
        for item in os.listdir(PAPER_DIR):
            item_path = os.path.join(PAPER_DIR, item)
            if os.path.isdir(item_path):
                file_path = os.path.join(item_path, "papers_info.json")
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as json_file:
                            papers_info = json.load(json_file)
                            if paper_id in papers_info:
                                return json.dumps(papers_info[paper_id], indent=2)
                    except (FileNotFoundError, json.JSONDecodeError):
                        continue
        return f"There's no saved information related to paper {paper_id}."

if __name__ == "__main__":
    server = MCPServer()
    # Example usage
    print(server.search_papers("machine learning", 2))
    print(server.extract_info("some_paper_id"))

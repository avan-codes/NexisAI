import httpx
from typing import Optional, Dict, Any
from ..core.config import settings

async def get_github_client(access_token: str) -> httpx.AsyncClient:
    return httpx.AsyncClient(headers={"Authorization": f"Bearer {access_token}"})

async def get_repo_tree(access_token: str, owner: str, repo: str, branch: str = "main") -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        data = response.json()
        if "tree" in data:
            return data["tree"]
        return []

async def create_branch(access_token: str, owner: str, repo: str, base_branch: str, new_branch: str) -> bool:
    async with httpx.AsyncClient() as client:
        # Get SHA of base branch
        ref_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{base_branch}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if ref_response.status_code != 200:
            return False
        sha = ref_response.json()["object"]["sha"]
        create_response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/git/refs",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"ref": f"refs/heads/{new_branch}", "sha": sha},
        )
        return create_response.status_code == 201

async def get_file_content(access_token: str, owner: str, repo: str, path: str, branch: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code == 200:
            import base64
            content = response.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
        return None

async def update_file_content(access_token: str, owner: str, repo: str, path: str, new_content: str, branch: str, commit_message: str) -> bool:
    async with httpx.AsyncClient() as client:
        # Get current file SHA
        file_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if file_response.status_code != 200:
            return False
        file_data = file_response.json()
        import base64
        encoded_content = base64.b64encode(new_content.encode()).decode()
        update_response = await client.put(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "message": commit_message,
                "content": encoded_content,
                "sha": file_data["sha"],
                "branch": branch,
            },
        )
        return update_response.status_code in [200, 201]

async def create_pull_request(access_token: str, owner: str, repo: str, branch: str, base: str, title: str, body: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/pulls",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"title": title, "head": branch, "base": base, "body": body},
        )
        return response.json()

async def handle_github_event(event: str, payload: dict):
    # Implement as needed: update execution based on push, PR, check_run events
    pass

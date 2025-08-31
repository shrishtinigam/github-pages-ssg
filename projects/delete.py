from db_utils.projects import project_exists, archive_project

def delete_project(slug: str) -> None:
    """
    Move a project to deleted_projects and remove it from projects.
    """
    if not project_exists(slug):
        print(f"❌ No project found with slug '{slug}'")
        return

    archive_project(slug)
    print(f"🗑️ Project '{slug}' moved to deleted_projects.")

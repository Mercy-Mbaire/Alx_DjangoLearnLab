# Tagging and Search Documentation

This guide explains how to use the tagging and search features in the Django Blog project.

## Tagging Posts

### How to add tags
When creating or editing a blog post, you will see a **Tags** field in the form.
- You can enter multiple tags separated by commas (e.g., `django, python, webdev`).
- Tags are automatically created if they don't exist.
- Existing tags will be associated with the post.

### Viewing tags
- Tags are displayed on each post in the blog feed and on the post detail page.
- Clicking on a tag will display a list of all posts associated with that tag.
- The URL for tag-filtered posts follows the format: `/tags/<tag_name>/`.

## Search Functionality

### How to search
A search bar is available in the header of every page.
- Enter keywords in the search box and press Enter or click the Search button.
- The search functionality looks for matches in:
    - **Post Title**
    - **Post Content**
    - **Associated Tags**

### Search Results
- If matches are found, you will be redirected to a search results page listing all relevant posts.
- If no matches are found, a message will indicate that no results were found.
- The search results page can be accessed directly at `/search/?q=<your_query>`.

## Technical Implementation Notes
- **Tagging**: Implemented using `django-taggit`.
- **Search**: Powered by Django `Q` objects for complex lookups across multiple fields.
- **Views**: 
    - `SearchResultsView` (ListView) for results.
    - `PostByTagListView` (ListView) for tag-based filtering.

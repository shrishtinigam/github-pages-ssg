
# Python Static Site Generator (SSG)

A lightweight static site generator built with Python and Jinja2.  
This project follows a simplified Model View Controller (MVC) pattern for clean separation of content, templates, and build logic.

## Features
- Write content in Python models (`entities/` folder)  
- Use Jinja2 templates (`templates/`) for layout and styling  
- Output clean static HTML to the `BASE_URL` folder  
- Easy to extend with new entities (Posts, Projects, Research, Exp etc.)  
- Supports custom styling with `static/` (CSS, JS, images)  

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/shrishtinigam/github-pages-ssg.git
cd github-pages-ssg
pip install -r requirements.txt
````

Dependencies:

* jinja2
* Markdown

## Usage

To build the site:

```bash
python controller/build.py
```

Your static site will be generated inside the BASE_URL folder. Open `BASE_URL/index.html` in your browser to preview.

## How It Works (WIP !)

1. **Models (entities/)**
   Each content type (e.g., `Post`) is defined as a Python class.

   Example:

   ```python
   from dataclasses import dataclass

   @dataclass
   class Post:
       title: str
       slug: str
       description: str
       body_html: str
   ```

2. **Views (templates/)**
   Jinja2 templates define how content is rendered.

   Example snippet from `index.html`:

   ```html
   {% for post in posts %}
     <h2><a href="{{ post.slug }}.html">{{ post.title }}</a></h2>
   {% endfor %}
   ```

3. **Controller (build.py)**
   The build script loads entities, passes them to templates, and writes static HTML files.

## Customization

* Modify `view/templates/base.html` and `view/static/style.css` for global layout
* Add your content in a `/content` directory

## Roadmap

* [ ] Deployment guide (GitHub Pages)
* [ ] Add OOPs based class structure to entities
* [ ] Add more entity types (Research, Job Experiences)

## License

MIT License


# Create a python pacage using GIT,GIHUB and POETRY

## Procjet setup
### make a new project
`poetry new fem_interface`

### project file structure
```plaintext
fem_interface/
├── pyproject.toml
├── fem_interface/
│   ├── __init__.py
│   ├── fem/
│   │   ├── __init__.py
│   │   ├── cards/
│   │   │   ├── __init__.py
│   │   │   └── beuslo.py
│   └── another_module.py
└── tests/
    ├── __init__.py
    └── test_beuslo.py
```

`cd fem_interface`

### Activating the virtual environment

`poetry shell`


### Specifying dependencies

`poetry add numpy`


### build  pacage 

`poetry build`

## setup Gihub
Create repostory on GITHUB named fem_interface

Create a new repostory on the command line

`git init`
`git add .`
`git commit -m "first commit" ` <br>
`git branch -M main`<br>
`git remote add origin https://github.com/sveinomork/fem_interface.git` <br>
`git push -u origin main`

# Clone the repostory
`git clone https://github.com/sveinomork/fem_interface.git fem_interface_clone`

`cd fem_interface_clone`



### Activating the virtual environment

`poetry shell`

### install 
`poetry install`


# install the pacage from github

## Procjet setup
### make a new project
`poetry new fem_interface_pacage`

`cd fem_interface_pacage`

### Activating the virtual environment

`poetry shell`


### Add the pacage

`poetry add git+https://github.com/sveinomork/fem_interface.git`

















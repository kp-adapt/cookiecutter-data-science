rule requirements:
    """Tests environment, and if correct, installs requirements.txt
    """
    run:
        correct_env_bool = True
        try:
            shell("python test_environment.py")
        except:
            correct_env_bool = False
            print("ERROR: packages were not installed. Incorrect env configuration. See test_environment.py")
        
        if correct_env_bool:
            shell("pip install -r requirements.txt")

rule create_venv:
    """Creates new conda virtual environment called "venv", overwriting existing 
    environments with the same name. Uses environment.yaml to install pip in the
    environment as well as requirements.
    """
    shell:
        """
        conda env create -n venv --file environment.yaml --force
        """

rule clean:
    """Removes pycache files and folders.
    """
    shell:
        """
        find . -type f -name "*.py[co]" -delete
	    find . -type d -name "__pycache__" -delete
        """

rule format:
    """Runs yapf over contents of src folder.
    """
    shell:
        """
        yapf -ir --style "google" src/
        """

rule help:
    """
    Print list of all targets with help.
    """
    run:
      for rule in workflow.rules:
        print(rule.name)
        print(rule.docstring)
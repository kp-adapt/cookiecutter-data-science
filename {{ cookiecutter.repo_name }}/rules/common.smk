rule requirements:
    run:
        correct_env_bool = True
        try:
            shell("python test_environment.py")
        except:
            correct_env_bool = False
            print("ERROR: packages were not installed. Incorrect env configuration. See test_environment.py")
        
        if correct_env_bool:
            shell("pip install -U pip setuptools wheel")
            shell("pip install -r requirements.txt")
rule clean:
    shell:
        """
        find . -type f -name "*.py[co]" -delete
	    find . -type d -name "__pycache__" -delete
        """

rule format:
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
      print( rule.name )
      print( rule.docstring )
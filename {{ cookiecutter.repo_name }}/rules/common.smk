rule requirements:
    shell:
        """
        python -m pip install -U pip setuptools wheel
        python -m pip install -r requirements.txt
        """

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
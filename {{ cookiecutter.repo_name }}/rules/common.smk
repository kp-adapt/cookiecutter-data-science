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
download:
	wget https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip ! unzip LD2011_2014.txt.zip

install:
	pip install -r requirements.txt

create:
	conda create --name temporal_fusion_transformer python=3.9 ipykernel

activate:
	conda activate temporal_fusion_transformer

deactivate:
	conda deactivate

run:
	python main.py

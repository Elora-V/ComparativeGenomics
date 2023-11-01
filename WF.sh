#!/bin/bash



##### PARAMETERS #####

. ./config.sh
while getopts prot:blast: flag
do
    case "${flag}" in
    	prot) fileprot=${OPTARG};;
        blast) resultBlast=${OPTARG};;         
    esac
done

if [ -z $fileprot ]
then $fileprot="prot.tar"
fi

##### END PARAMETERS #




##### MAIN #####

# Download blast
if [ ! -f ncbi-blast-2.14.1+-x64-linux.tar.gz ]
then
wget  https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.14.1+-x64-linux.tar.gz
tar -zxvf ncbi-blast-2.14.1+-x64-linux.tar.gz
fi

# directory of protein in genomes 
if [ ! -d $path_to_prot_file ]
then tar -xvf $fileprot -C $path_to_prot_file
fi

# directory of genome database
if [ ! -d $path_to_db ]
then mkdir $path_to_db
fi


# make database and blast with ncbi
if [ -z $resultBlast ]
then 
	# recupère resultat déjà prêt
	if [ ! -d $path_to_blast_out ]
	then mkdir $path_to_blast_out 
	fi
	if if [[ $resultBlast == *.tar ]]
	then tar -xvf $resultBlast -C $path_to_blast_out
	else mv $resultBlast $path_to_blast_out
	fi

else
	# script qui renvoie les outputs
	chmod +x ./blast_db_creation.sh
	chmod +x ./launch_blast.sh
	./blast_db_creation.sh
	./launch_blast.sh
fi


#!/bin/bash



##### PARAMETERS #####

. ./config.sh

fileprot="prot.tar" # default value

while getopts p:b: flag
do
    case "${flag}" in
    	p) fileprot=${OPTARG};;
        b) resultBlast=${OPTARG};;       
    esac
done

##### END PARAMETERS #




##### MAIN #####

### Download blast ###

echo ""
echo "#########################################################"  
echo "Telechargement Blast"
echo "#########################################################"
echo ""

if [ ! -f ncbi-blast-2.14.1+-x64-linux.tar.gz ]
then
	wget  https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.14.1+-x64-linux.tar.gz
	tar -zxvf ncbi-blast-2.14.1+-x64-linux.tar.gz
else echo "already done"
fi

### Get proteins files ###
echo ""
echo "#########################################################"  
echo "Get proteins file"
echo "#########################################################"
echo ""

if [ ! -d $path_to_prot_file ]
then 
	mkdir $path_to_prot_file

	case $fileprot in
    *.tar|*.tar.gz)
		# dezip
        tar -xvf $fileprot 
        ;;
    *)
		# move
        mv ${fileprot}/* $path_to_prot_file
        ;;
	esac
fi

### Blast ###

echo ""
echo "#########################################################"  
echo "Blast"
echo "#########################################################"
echo ""
# directory of genome database
if [ ! -d $path_to_db ]
then mkdir $path_to_db
fi
# make database and blast with ncbi
if [ ! -z $resultBlast ]
then 
	# get result directly in directory
	if [ ! -d $path_to_blast_out ]
	then mkdir $path_to_blast_out 
	fi
	
	
	case $resultBlast in
    	*.tar|*.tar.gz)
			# dezip
			tar -xvf $resultBlast -C $path_to_blast_out ;;
		*)
			# move
			mv $resultBlast $path_to_blast_out ;;
	esac

else
	# execution script
	chmod +x ./modules/blast_db_creation.sh
	chmod +x ./modules/launch_blast.sh
	./modules/blast_db_creation.sh
	./modules/launch_blast.sh
fi


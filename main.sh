#!/bin/bash



##### PARAMETERS #####

. ./config.sh
evalue="1e-10"
id="30"
cov="50"


# default value

fileprot="prot.tar"

while getopts p:b:e:c:i flag
do
    case "${flag}" in
    	p) fileprot=${OPTARG};;
        b) resultBlast=${OPTARG};; 
		#e) evalue=${OPTARG};;  
		#c) coverage=${OPTARG};;  
		#i) identity=${OPTARG};;        
    esac
done


# if [ -z "$evalue" ]
# then evalue=""
# else evalue="-e '$evalue'"
# fi

# if [ -z "$coverage" ]
# then coverage=""
# else coverage="-cov '$coverage'"
# fi

# if [ -z "$identity" ]
# then identity=""
# else identity="-id '$identity'"
# fi

##### END PARAMETERS #




##### MAIN #####

### Download blast ###

echo ""
echo "#########################################################"  
echo "Telechargement Blast"
echo "#########################################################"
echo ""

if [ ! -f ncbi-blast-2.15.0+-x64-linux.tar.gz ]
then
	wget  https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.15.0+-x64-linux.tar.gz
	tar -zxvf ncbi-blast-2.15.0+-x64-linux.tar.gz
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
else
	echo "already done"
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
	echo "Get output blast"
	# get result directly in directory
	if [ ! -d $path_to_blast_out ]
	then mkdir $path_to_blast_out 
	
	
		case $resultBlast in
			*.tar|*.tar.gz)
				# dezip
				tar -xvf $resultBlast -C $path_to_blast_out ;;
			*)
				# move
				mv $resultBlast $path_to_blast_out ;;
		esac
	else echo "already done"
	fi

else
	echo " Execution of blast"
	# execution script
	chmod +x ./modules/blast_db_creation.sh
	chmod +x ./modules/launch_blast.sh
	./modules/blast_db_creation.sh
	./modules/launch_blast.sh
fi

### Blast output parser ###


# if [ ! -f $outputDico ] 
# then 

# 	echo ""
# 	echo "#########################################################"  
# 	echo "Blast output parser"
# 	echo "#########################################################"
# 	echo ""
# 	python3 modules/Path_Blast.py -d $path_to_blast_out -j $outputDico -e $evalue -cov $cov -id $id

# 	echo ""
# 	echo "#########################################################"  
# 	echo "Recherche core genome"
# 	echo "#########################################################"
# 	echo ""
# 	python3 modules/clique.py -f $outputDico

# fi

if [ ! -f "$outputCDS" ] || [ ! -f "$outputIgorf" ]
then
echo ""
echo "#########################################################"  
echo "Blast output parser"
echo "#########################################################"
echo ""
python3 modules/Parse_CDS_IGORF.py -d Blast_output_igorf -jcds $outputCDS -jigorf $outputIgorf \
-ecds 1e-5 -idcds 30 -covcds 70 -eigorf 1e-5 -idigorf 30 -covigorf 70 -ocds "coreCDS.txt" -oigorf "coreIGORF.txt"
fi


echo ""
echo "#########################################################"  
echo "Recherche core genome"
echo "#########################################################"
echo ""
python3 modules/clique.py -f $outputCDS -o "coreCDS.txt"
python3 modules/clique.py -f $outputIgorf -o "coreIGORF.txt"
rm $outputCDS
rm $outputIgorf 


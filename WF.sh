#!/bin/bash



if [ ! -f ncbi-blast-2.14.1+-x64-linux.tar.gz ]
then
wget  https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.14.1+-x64-linux.tar.gz
tar -zxvf ncbi-blast-2.14.1+-x64-linux.tar.gz
fi


if [ ! -d prot ]
then tar -xvf prot.tar
fi

if [ ! -d Blast_db ]
then mkdir Blast_db
fi

chmod +x ./blast_db_creation.sh
./blast_db_creation.sh



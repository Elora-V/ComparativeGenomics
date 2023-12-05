####################################
#  Genomique comparée 
####################################
setwd("~/Documents/M2_AMI2B/ComparativeGenomics")
rm(list=ls())

cds=read.table("coreCDS.txt",header = T, sep="\t")
igorf=read.table("coreIGORF.txt",header = T, sep="\t")

# quand id fixé, et cov diffère
cds_cov= unique(cds[cds$id==30,])
cds_cov=cds_cov[order(cds_cov$cov), ]
igorf_cov= unique(igorf[igorf$id==30,])
igorf_cov=igorf_cov[order(igorf_cov$cov), ]
plot(cds_cov$coreGenome~cds_cov$cov,type="l",main="Core genome CDS en fonction coverage")
plot(igorf_cov$coreGenome~igorf_cov$cov,type="l",main="Core genome igorf en fonction coverage")

# qd cov fixé et id diffère
cds_id= unique(cds[cds$cov==70,])
cds_id=cds_id[order(cds_id$id), ]
igorf_id= unique(igorf[igorf$cov==70,])
igorf_id=igorf_id[order(igorf_id$id), ]
plot(cds_id$coreGenome~cds_id$id,type="l",main="Core genome CDS en fonction id")
plot(igorf_id$coreGenome~igorf_id$id,type="l",main="Core genome igorf en fonction id")


population_data_files_url <- 'http://www2.census.gov/acs2013_1yr/pums/csv_pus.zip'
housing_data_files_url <- 'http://www2.census.gov/acs2013_1yr/pums/csv_hus.zip'

library(RCurl)

population_data_file <- getBinaryURL(population_data_files_url)

housing_data_file <- getBinaryURL(housing_data_files_url)

population_data_file_path <- '/vault-econ/SparkR/2013-acs/csv_pus.zip'
population_data_file_local <- file(population_data_file_path, open = "wb")
writeBin(population_data_file, population_data_file_local)
close(population_data_file_local)

housing_data_file_path <- '/nfs/data/2013-acs/csv_hus.zip'
housing_data_file_local <- file(housing_data_file_path, open = "wb")
writeBin(housing_data_file, housing_data_file_local)
close(housing_data_file_local)

data_file_path <- '/nfs/data/2013-acs'
unzip(population_data_file_path, exdir=data_file_path)

unzip(housing_data_file_path, exdir=data_file_path)

#Setup Spark

Sys.setenv(SPARK_HOME='/home/cluster/spark-1.5.0-bin-hadoop2.6')
.libPaths(c(file.path(Sys.getenv('SPARK_HOME'), 'R', 'lib'), .libPaths()))

library(SparkR)


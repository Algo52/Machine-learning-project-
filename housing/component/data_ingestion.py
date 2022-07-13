
import imp
from logging import exception
from turtle import pd
from housing.entity.config_entity import DataIgestionConfig
from housing.exception import HousingException
import sys,os,tarfile
from six.moves import urllib    ###to extract the zip file
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit





class DataIngestion:

    def __init__(self,data_ingestion_config:DataIgestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys)
    

    def download_housing_data(self,) -> str:
        try:
            ##extracting removte url to download dataset
            download_url=self.data_ingestion_config.dataset_download_url
            
            ##folder location to download file
            tgz_download_dir=self.data_ingestion_config.tz_download_dir

            ## CHECKING PATH EXIT AR NOT
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
        
            ### creating a folder if it is not avaliable
            os.makedirs(tgz_download_dir,exist_ok=TRUE)

            ## file name
            housing_file_name=os.path.basename(download_url)

            ## complete file path
            tgz_file_path=os.path.join(tgz_download_dir,housing_file_name)

            logging.info(f"(Download file from: [{download_url}] into:[{tgz_file_path}]")

            ##to extract the file 
            urllib.request.urlretrieve(download_url,tgz_file_path)


            logging.info(f"File:[{tgz_file_path}] has been downloaded sucessfully")
            ## return the location
            return tgz_file_path


        except Exception as e:
            raise HousingException(e,sys) from e




    

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            ## giving location to extract the file
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            ## CHECKING PATH EXIT AR NOT
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
        
            ### creating a folder if it is not avaliable
            os.makedirs(raw_data_dir,exist_ok=True)
            
            logging.info(f"Extracting tgxfile:[{tgz_file_path}] into [{raw_data_dir}]")

            ## read tgz file and extract
            with tarfile.open(tgz_file_path) as  housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(data=raw_data_dir)
            logging.info(f"Exctraction Completed")
            
            
        except Exception as e:
            raise HousingException(e,sys) from e

   
   
   
   
    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            ##giving file name with os
            file_name=os.listdir(raw_data_dir)[0]

            housing_file_path=os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file: [{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)
            
            ## creating 5 grops with numpy and dividing dataset
            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)
            
            ## giving file path
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_data,file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_data,file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_data,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_data, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
           
           
            data_ingestion_artifact = DataIngestionArtifact(
                                train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
             
             
            return data_ingestion_artifact



        except Exception as e:
            raise HousingException(e,sys) from e



    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path =  self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")

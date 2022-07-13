## defing a structure or entity
from collections import namedtuple


DataIgestionConfig=namedtuple("DataIgestionConfig",
["dataset_download_url","tz_download_dir","raw_data_dir","ingested_train_data","ingested_test_data"])


DataValidationConfig= namedtuple("DataIgestionConfig",["schema_file_path"])

DataTransformationConfig=namedtuple("DataTransformationConfig",["add_bedroom_per_room",
                                                                "transformed_train_dir",
                                                                "transformed_test_dir",
                                                                "preprocessed_object_file_path"])

MOdelTrainerConfig=namedtuple("MOdelTrainerConfig", ["trained_model_file_path","base_accuracy"])             

ModelEvaluationConfig=namedtuple("ModelEvaluationConfig" , ["model_evaluation_file_path","time_stamp"])

ModelPusherConfig=namedtuple("ModelPusherConfig",["export_dir_path"])

TainingPipelineConfig=namedtuple("TainingPipelineConfig",["artifact_dir"])


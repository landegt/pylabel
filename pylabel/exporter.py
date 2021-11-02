import json
from typing import List
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os 
from pathlib import PurePath, Path

class Export():
    def  __init__(self, dataset=None):
        self.dataset = dataset
        
    def ExportToVoc(self, output_path=None, segmented_=False, path_=False, database_=False, folder_=False, occluded_=False):
        ds = self.dataset

        if output_path == None:
            output_path = ds.path_to_annotations
        else:        
            output_path = output_path

        os.makedirs(output_path, exist_ok=True)

        """ Writes annotation files to disk in VOC XML format and returns path to files.

        By default, tags with empty values will not be included in the XML output. 
        You can optionally choose to include them if they are required for your solution.

        Args:
            dataset (obj): 
                A dataset object that contains the annotations and metadata.
            output_path (str or None): 
                This is where the annotation files will be written.
                If not-specified then the path will be derived from the .path_to_annotations and
                .name properties of the dataset object. 

        Returns:
            A list with 1 or more paths (strings) to annotations files.
        """   
        output_file_paths = []

        def voc_xml_file_creation(data, file_name, output_file_path, segmented=True, path=True, database=True, folder=True, occluded=True):
         
            index = 0
            df_smaller = data[data['img_filename'] == file_name].reset_index()
            
            if len(df_smaller) == 1:
                #print('test')
                annotation_text_start = '<annotation>'

                flder_lkp = str(df_smaller.loc[index]['img_folder'])
                if folder==True and flder_lkp != '':
                    folder_text = '<folder>'+flder_lkp+'</folder>'
                else:
                    folder_text = ''
                    
                filename_text = '<filename>'+str(df_smaller.loc[index]['img_filename'])+'</filename>'
                
                pth_lkp = str(df_smaller.loc[index]['img_path'])
                if path == True and pth_lkp != '':
                    path_text = '<path>'+ pth_lkp +'</path>'
                else:
                    path_text = ''
                    
                sources_text = ''
                
                size_text_start = '<size>'
                width_text = '<width>'+str(df_smaller.loc[index]['img_width'])+'</width>'
                height_text = '<height>'+str(df_smaller.loc[index]['img_height'])+'</height>'
                depth_text = '<depth>'+str(df_smaller.loc[index]['img_depth'])+'</depth>'
                size_text_end = '</size>'
                
                seg_lkp = str(df_smaller.loc[index]['ann_segmented'])
                if segmented == True and seg_lkp != '':
                    segmented_text = '<segmented>'+str(df_smaller.loc[index]['ann_segmented'])+'</segmented>'
                else:
                    segmented_text = ''

                object_text_start = '<object>'

                name_text = '<name>'+str(df_smaller.loc[index]['cat_name'])+'</name>'
                pose_text = '<pose>'+str(df_smaller.loc[index]['ann_pose'])+'</pose>'
                truncated_text = '<truncated>'+str(df_smaller.loc[index]['ann_truncated'])+'</truncated>'
                difficult_text = '<difficult>'+str(df_smaller.loc[index]['ann_difficult'])+'</difficult>'
                
                occluded_text = ''

                bound_box_text_start = '<bndbox>'

                xmin_text = '<xmin>'+str(df_smaller.loc[index]['ann_bbox_xmin'])+'</xmin>'
                xmax_text = '<xmax>'+str(df_smaller.loc[index]['ann_bbox_xmax'])+'</xmax>'
                ymin_text = '<ymin>'+str(df_smaller.loc[index]['ann_bbox_ymin'])+'</ymin>'
                ymax_text = '<ymax>'+str(df_smaller.loc[index]['ann_bbox_ymax'])+'</ymax>'

                bound_box_text_end = '</bndbox>'
                object_text_end = '</object>'
                annotation_text_end = '</annotation>'
                        
                xmlstring = annotation_text_start + folder_text  +filename_text  + \
                    path_text  + sources_text + size_text_start + width_text  + \
                    height_text  + depth_text  + size_text_end + segmented_text  + \
                    object_text_start + name_text  + pose_text  +truncated_text + \
                    difficult_text + occluded_text + bound_box_text_start  +xmin_text  + \
                    xmax_text  +ymin_text  +ymax_text  +bound_box_text_end  + \
                    object_text_end  + annotation_text_end
                dom = xml.dom.minidom.parseString(xmlstring)
                pretty_xml_as_string = dom.toprettyxml()
                
                with open(output_file_path, "w") as f:
                    f.write(pretty_xml_as_string)    

                return output_file_path
            
            else:

                #print('test')
                annotation_text_start = '<annotation>'
                
                flder_lkp = str(df_smaller.loc[index]['img_folder'])
                if folder==True and flder_lkp != '':
                    folder_text = '<folder>'+flder_lkp+'</folder>'
                else:
                    folder_text = ''
                
                filename_text = '<filename>'+str(df_smaller.loc[index]['img_filename'])+'</filename>'
                
                pth_lkp = str(df_smaller.loc[index]['img_path'])
                if path == True and pth_lkp != '':
                    path_text = '<path>'+ pth_lkp +'</path>'
                else:
                    path_text = ''
                
                #db_lkp = str(df_smaller.loc[index]['Databases'])
                #if database == True and db_lkp != '':
                #    sources_text = '<source>'+'<database>'+ db_lkp +'</database>'+'</source>'
                #else:
                sources_text = ''
                    
                size_text_start = '<size>'
                width_text = '<width>'+str(df_smaller.loc[index]['img_width'])+'</width>'
                height_text = '<height>'+str(df_smaller.loc[index]['img_height'])+'</height>'
                depth_text = '<depth>'+str(df_smaller.loc[index]['img_depth'])+'</depth>'
                size_text_end = '</size>'
                
                seg_lkp = str(df_smaller.loc[index]['ann_segmented'])
                if segmented == True and seg_lkp != '':
                    segmented_text = '<segmented>'+str(df_smaller.loc[index]['ann_segmented'])+'</segmented>'
                else:
                    segmented_text = ''

                xmlstring = annotation_text_start + folder_text  +filename_text  + \
                        path_text  + sources_text + size_text_start + width_text  + \
                        height_text  + depth_text  + size_text_end + segmented_text
                
                for obj in range(len(df_smaller)):
                    object_text_start = '<object>'

                    name_text = '<name>'+str(df_smaller.loc[index]['cat_name'])+'</name>'
                    pose_text = '<pose>'+str(df_smaller.loc[index]['ann_pose'])+'</pose>'
                    truncated_text = '<truncated>'+str(df_smaller.loc[index]['ann_truncated'])+'</truncated>'
                    difficult_text = '<difficult>'+str(df_smaller.loc[index]['ann_difficult'])+'</difficult>'
                    
                    #occ_lkp = str(df_smaller.loc[index]['Object Occluded'])
                    #if occluded==True and occ_lkp != '':
                    #    occluded_text = '<occluded>'+occ_lkp+'</occluded>'
                    #else:
                    occluded_text = ''

                    bound_box_text_start = '<bndbox>'

                    xmin_text = '<xmin>'+str(df_smaller.loc[index]['ann_bbox_xmin'])+'</xmin>'
                    xmax_text = '<xmax>'+str(df_smaller.loc[index]['ann_bbox_xmax'])+'</xmax>'
                    ymin_text = '<ymin>'+str(df_smaller.loc[index]['ann_bbox_ymin'])+'</ymin>'
                    ymax_text = '<ymax>'+str(df_smaller.loc[index]['ann_bbox_ymax'])+'</ymax>'

                    bound_box_text_end = '</bndbox>'
                    object_text_end = '</object>'
                    annotation_text_end = '</annotation>'
                    index = index + 1

                    xmlstring = xmlstring + object_text_start + name_text  + pose_text  +truncated_text + \
                        difficult_text + occluded_text + bound_box_text_start  +xmin_text  + \
                        xmax_text  +ymin_text  +ymax_text  +bound_box_text_end  + \
                        object_text_end  

                xmlstring = xmlstring + annotation_text_end
                dom = xml.dom.minidom.parseString(xmlstring)
                pretty_xml_as_string = dom.toprettyxml()
                
                with open(output_file_path, "w") as f:
                    f.write(pretty_xml_as_string)  

                return output_file_path

        #Loop through all images in the dataframe and call voc_xml_file_creation for each one
        for file_title in list(set(self.dataset.df.img_filename)):

            file_name = Path(file_title)
            file_name = str(file_name.with_suffix('.xml'))
            file_path = str(Path(output_path, file_name))
            voc_file_path = voc_xml_file_creation(ds.df, file_title, segmented=segmented_, path=path_, database=database_, folder=folder_, occluded=occluded_, output_file_path=file_path)
            output_file_paths.append(voc_file_path)

        return output_file_paths

    def ExportToYoloV5(self, output_path=None):
        """ Writes annotation files to disk and returns path to files.
        
        Args:
            dataset (obj): 
                A dataset object that contains the annotations and metadata.
            output_path (str or None): 
                This is where the annotation files will be written.
                If not-specified then the path will be derived from the .path_to_annotations and
                .name properties of the dataset object. 

        Returns:
            A list with 1 or more paths (strings) to annotations files.
        """
        ds = self.dataset
        #Inspired by https://github.com/aws-samples/groundtruth-object-detection/blob/master/create_annot.py 
        unique_images = ds.df["img_filename"].unique()
        output_file_paths = []

        yolo_dataset = ds.df.copy(deep=True)
        yolo_dataset.cat_id = yolo_dataset.cat_id.astype('float').astype('Int32')
        yolo_dataset["center_x_scaled"] = (yolo_dataset["ann_bbox_xmin"] + (yolo_dataset["ann_bbox_width"]*0.5))/yolo_dataset["img_width"]
        yolo_dataset["center_y_scaled"] = (yolo_dataset["ann_bbox_ymin"] + (yolo_dataset["ann_bbox_height"]*0.5))/yolo_dataset["img_height"]
        yolo_dataset["width_scaled"] = yolo_dataset["ann_bbox_width"] / yolo_dataset["img_width"]
        yolo_dataset["height_scaled"] = yolo_dataset["ann_bbox_height"] / yolo_dataset["img_height"]
        yolo_dataset[["cat_id", "center_x_scaled", "center_y_scaled", "width_scaled", "height_scaled"]]

        #Create folders to store annotations
        if output_path == None:
            dest_folder = PurePath(ds.path_to_annotations, yolo_dataset.iloc[0].img_folder)
        else:
            dest_folder = output_path

        os.makedirs(dest_folder, exist_ok=True)

        for img_filename in unique_images:
                df_single_img_annots = yolo_dataset.loc[yolo_dataset.img_filename == img_filename]
                annot_txt_file = img_filename.split(".")[0] + ".txt"
                destination = f"{dest_folder}/{annot_txt_file}"
                df_single_img_annots.to_csv(
                    destination,
                    index=False,
                    header=False,
                    sep=" ",
                    float_format="%.4f",
                    columns=[
                        "cat_id",
                        "center_x_scaled",
                        "center_y_scaled",
                        "width_scaled",
                        "height_scaled",
                    ])
                output_file_paths.append(destination)

        return output_file_paths

    def ExportToCoco(self, output_path=None) -> List:
        """ 
        Writes annotation files to disk and returns path to files.

        Args:
            dataset (obj): 
                A dataset object that contains the annotations and metadata.
            output_path (str or None): 
                This is where the annotation files will be written.
                If not-specified then the path will be derived from the .path_to_annotations and
                .name properties of the dataset object. 

        Returns:
            A list with 1 or more paths (strings) to annotations files.
        """
        df = self.dataset.df
        df_outputI = []
        df_outputA = []
        df_outputC = []
        list_i = []
        list_c = []
        json_list = []
        
        for i in range(0,df.shape[0]):
            images = [{
            "id": df['img_id'][i], 
            "folder": df['img_folder'][i], 
            "file_name": df['img_filename'][i], 
            "path": df['img_path'][i], 
            "width": df['img_width'][i], 
            "height": df['img_height'][i], 
            "depth": df['img_depth'][i]
            }]
        
            annotations = [{
            "image_id": df['img_id'][i], 
            "id": df.index[i], 
            "segmented": df['ann_segmented'][i],
            "bbox": [df['ann_bbox_xmin'][i], df['ann_bbox_ymin'][i], df['ann_bbox_width'][i], df['ann_bbox_height'][i]],  
            "area": df['ann_area'][i], 
            "segmentation": df['ann_segmentation'][i], 
            "iscrowd": df['ann_iscrowd'][i], 
            "pose": df['ann_pose'][i], 
            "truncated": df['ann_truncated'][i],
            "category_id": df['cat_id'][i],  
            "difficult": df['ann_difficult'][i]
            }]

            categories = [{
            "id": int(df['cat_id'][i]), 
            "name": df['cat_name'][i], 
            "supercategory": df['cat_supercategory'][i]
            }]
            
            if(list_c):
                if (categories[0]["id"] in list_c or np.isnan(categories[0]["id"])):
                    pass    
                else:
                    df_outputC.append(pd.DataFrame([categories]))
            elif(~np.isnan(categories[0]["id"])):
                df_outputC.append(pd.DataFrame([categories]))
            else:
                pass
            list_c.append(categories[0]["id"])

            if(list_i):
                if (images[0]["id"] in list_i or np.isnan(images[0]["id"])):
                    pass
                else:
                    df_outputI.append(pd.DataFrame([images]))
            elif(~np.isnan(images[0]["id"])):
                df_outputI.append(pd.DataFrame([images]))      
            else:
                pass
            list_i.append(images[0]["id"])    

            df_outputA.append(pd.DataFrame([annotations]))
            
        mergedI = pd.concat(df_outputI, ignore_index=True)
        mergedA = pd.concat(df_outputA, ignore_index=True)
        mergedC = pd.concat(df_outputC, ignore_index=True)
        
        resultI = mergedI[0].to_json(orient="split")
        resultA = mergedA[0].to_json(orient="split")
        resultC = mergedC[0].to_json(orient="split")

        parsedI = json.loads(resultI)
        del parsedI['index']
        del parsedI['name']
        parsedI['images'] = parsedI['data']
        del parsedI['data']

        parsedA = json.loads(resultA)
        del parsedA['index']
        del parsedA['name']
        parsedA['annotations'] = parsedA['data']
        del parsedA['data']

        parsedC = json.loads(resultC)
        del parsedC['index']
        del parsedC['name']
        parsedC['categories'] = parsedC['data']
        del parsedC['data']

        parsedI.update(parsedA)
        parsedI.update(parsedC)
        json_output = parsedI

        if output_path == None:
            output_path = Path(self.dataset.path_to_annotations, (self.dataset.name + ".json"))
            
        with open(output_path, 'w') as outfile:
            json.dump(obj=json_output, fp=outfile, indent=4)
        return [str(output_path)] 
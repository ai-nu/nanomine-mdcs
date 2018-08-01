function MAIN(user_name,input_type,num_recon,file_name)
% function MAIN(img_name, type, cutL, VF, recon_length, scale, visualize_fine_recon, visualize_coarse_recon, workingdir)
%
% This package is developed by Hongyi Xu, Northwestern University
% PI: Prof. Wei Chen, Northwestern University
% Contact: hongyixu2014@u.northwestern.edu
% Modified for NANOMINE by: Akshay Iyer; 13th Feb. 2018

%%% Input Types %%
% 1 : Single JPEG Image
% 2 : ZIP file containing JPEG images
% 3 : Image in .mat file
%%
%% Create Job ID and encrypt it %%
c = clock;  % To record temporal details
year = c(1); month = c(2); date = c(3);hour=c(4); minute=c(5); seconds=c(6); % define all time related variables
c(1) = c(1) + 7;
c(2) = c(2) + 13;
c(3) = c(3) + 17;
Job_ID = [num2str(c(2)),num2str(c(3)),num2str(c(4)),fliplr(num2str(c(1))),num2str(c(5)),num2str(c(6))];
%%%

time_stamp = ['H',num2str(hour),'/','M',num2str(minute)]; % create a time stamp to store files

if month < 10 % convert single digit to double
    str_month = ['0',num2str(month)];
else
    str_month = num2str(month);
end

if date < 10
   str_date = ['0',num2str(date)];
else
   str_date = num2str(date);
end

%% Write to Activity log %%
time_now= [num2str(year),':',num2str(month),':',num2str(date),':',num2str(hour),':',num2str(minute),':',num2str(seconds)];
user_activity = [time_now,' ',(user_name),' ','Reconstruction - Descriptor',' ',Job_ID];
addpath('/home/NANOMINE/Develop/mdcs');
fileID = fopen('/home/NANOMINE/Production/mdcs/Activity_log.txt','a+');
fprintf(fileID,'\n%s\n',user_activity);
fclose(fileID);

stamp = [num2str(year),'/',str_month,'/',str_date,'/'];

path_to_file = ['../media/documents/',stamp]; 

fname = file_name; % incoming file name
path_to_write = ['/var/www/html/nm/Descriptor/Reconstruction/',Job_ID];
mkdir(path_to_write);

%% Specify import function according to input option
switch input_type
    case 1
        img = imread([path_to_file,fname]); % read the incming target and store pixel values
        
        if size(img) > 1
            img_original = img(:,:,1);
	else
	    img_original = img;
        end
        if max(img_original(:)) > 1
            img_original = round(img_original/256);
	    imwrite(img,[path_to_write,'/','Input.jpg'])
	else
	    imwrite(256*img,[path_to_write,'/','Input.jpg'])
        end
    case 2 
        unzip([path_to_file,fname],[path_to_write,'/input']);
    case 3
        load([path_to_file,fname]);
        img_original = Input;
        imwrite(256*img_original,[path_to_write,'/','Input.jpg']);
end

%% Define useful variables as required by package %%
img = img_original;
type = 0; % this webtool is for binary images only
cutL = size(img_original,1);
VF = mean(img_original(:));
recon_length = size(img_original,1); % size of reconstructed volume : recon_length-by-recon_length-by-recon_length
scale = 50; % for a 50-by-50-by-50 coarse reconstruction needed for FEA
visualize_fine_recon = 0;
visualize_coarse_recon = 0;
workingdir = path_to_write;
addpath('./recon_algorithm'); addpath(workingdir);
%cd('./recon_algorithm')  % go to the working directory

%% II: Characterization. User-operation required (2 out of 2)
if type == 0 % if it is a binary image
    
    Descriptor_C2_Binary(path_to_write,img, VF, recon_length)
    
else  % If it is a greyscale image

    % Step 1: image preprocessing
    Descriptor_C1(img, VF, cutL);

    % ------------------------- IMAGEJ Operation ------------------------------
    % Step 2: operating imageJ (following the manual). IMAGEJ OPERATION NEEDED.
    disp('Do NOT clost MATLAB. Please keep it on and minimize the window.')
    disp('Then follow the manual to operate IMAGEJ.')
    disp('After generating "cllist.txt" in working directory,')
    disp('go back to MATLAB and press anykey to continue...')
    pause
    % -------------------------------------------------------------------------

    % Step 3: 2D characterization and 3D prediction
    Descriptor_C2(img, VF, recon_length);
    
end

%% III: Reconstruction
%cd('./recon_algorithm')  % go to the working directory
img_name = [path_to_write,'/Input'];
load( [ img_name, '_GB_double_filter_3D_results.mat' ] ); % Load characterization results, which include a variable "name" (= img_name)
clearvars -except  img_original path_to_write Job_ID user_name num_recon name  recon_length  VF  N  num_3D ND3D  Predict_3D_As_mean  Predict_3D_As_var scale  visualize_fine_recon  visualize_coarse_recon  type % only keep the useful variables

% Start microstrutcure reconstruction
name_3D = [name, '_3D_recon'];
Descriptor_Recon_3D(name_3D, recon_length, VF, round(num_3D), ND3D, Predict_3D_As_mean, Predict_3D_As_var);

clearvars -except  img_original path_to_write Job_ID user_name num_recon name  name_3D  scale  visualize_fine_recon  visualize_coarse_recon  type  img_name 
clc


%% IV: Rescale the large reconstruction into a small one
% Here the 300x300x300 is rescaled into a smaller 60x60x60 structure (for FEA)
load( [name_3D, '.mat'] )
% clear -except  name img  img_original scale  visualize_fine_recon  visualize_coarse_recon

%[ img_coarse, Bimg_coarse ] = fine2coarse(img, scale);
%save( [ name, '_coarsen_recon.mat'], 'img_coarse', 'Bimg_coarse' )

% 
%% VII: Visualization
if visualize_coarse_recon == 1
    cord = ThreeD2Coordinate(Bimg_coarse);
    figure('color',[1,1,1]);
    voxel_image( cord, 1, 'g', 0.5, 'b' ); 
    axis equal
    box on
    L = length(Bimg_coarse);
    axis([1 L 1 L 1 L])
    view([1,0.5,0.5])
    saveas(gcf,[path_to_write,'/Coarse_recon.jpg']);
    saveas(gcf,[path_to_write,'/Coarse_recon.fig']);
end

if visualize_fine_recon == 1
    cord = ThreeD2Coordinate(img);
    figure('color',[1,1,1]);
    voxel_image( cord, 1, 'g', 0.5, 'b' ); 
    axis equal
    box on
    L = length(img);
    axis([1 L 1 L 1 L])
    view([1,0.5,0.5])
    saveas(gcf,[path_to_write,'/Fine_recon.jpg']);
end

% plot correlation 
Plot_Correlation(img_original, img, path_to_write);
%  clc
disp('The 3D descriptor-based C&R is completed!')

% delete unwanted files
cd(path_to_write);
delete Input_GB_double_filter_3D_results.mat;
delete Input_GB_double_filter_2D_results.mat;
%% ZIP files %%
zip([path_to_write,'/Results.zip'],{'*'},path_to_write);

%% Email to user%%
To = ['To:',user_name];
Subject = ['Subject: Reconstruction complete for Job ID: ',Job_ID];
Content = 'Content-Type:text/html; charset="us-ascii"';
html_headers = '<html><body>';
%NM_logo = '<img src=''http://129.105.90.149/nm/NanoMine-logo.JPG''>';
Body1 = '<p>Greeting from NanoMine!</p>';
Body2 = '<p>You are receiving this email because you had submitted an image for reconstruction using Physical Descriptors.';
Body3 = ['The reconstruction process is complete and you can view the results','<a href= http://nanomine.northwestern.edu:8000/RECON_view_Result.html?foo=',num2str(Job_ID),'&submit=Send> here</a></p>'];
Body4 = '<p>Best Wishes,</p>';
Body5 = '<p>NanoMine Team.</p>';
Footer1 = '<p>***DO NOT REPLY TO THIS EMAIL***</p>';
html_footer = '</body></html>';
Body = [Body2,Body3];

fileID = fopen('/home/NANOMINE/Production/mdcs/RECON/email.html','wt+');
fprintf(fileID,'%s\n',To);
fprintf(fileID,'%s\n',Subject);
fprintf(fileID,'%s\n',Content);
fprintf(fileID,'%s\n',html_headers);
%fprintf(fileID,'%s\n',NM_logo);
fprintf(fileID,'\n%s\n',Body1);
fprintf(fileID,'\n%s\n',Body);
fprintf(fileID,'\n%s\n',Body4);
fprintf(fileID,'%s\n',Body5);
fprintf(fileID,'\n%s\n',Footer1);
fprintf(fileID,'%s\n',html_footer);
fclose(fileID);
end
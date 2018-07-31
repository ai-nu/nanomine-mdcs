function run_descchar(user_name,input_type,file_name)

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
user_activity = [time_now,' ',(user_name),' ','Characterization - Descriptor',' ',Job_ID];
addpath('/home/NANOMINE/Develop/mdcs');
fileID = fopen('/home/NANOMINE/Production/mdcs/Activity_log.txt','a+');
fprintf(fileID,'\n%s\n',user_activity);
fclose(fileID);

stamp = [num2str(year),'/',str_month,'/',str_date,'/'];

path_to_file = ['../media/documents/',stamp]; 

fname = file_name; % incoming file name
path_to_write = ['/var/www/html/nm/Descriptor/Characterization/',Job_ID];
mkdir(path_to_write);

%% Specify import function according to input option
switch input_type
    case 1
        img = imread([path_to_file,fname]); % read the incming target and store pixel values
        if size(img) > 1
            imwrite(img(:,:,1),[path_to_write,'/','Input1.jpg'])
        end
    case 2 
        img = unzip([path_to_file,fname],[path_to_write,'/input']);
    case 3
        load([path_to_file,fname]);
        img = Input;
        imwrite(img,[path_to_write,'/','Input1.jpg']);
end




% % filename of the most recently uploaded
% fname = f(fid).name; 
% [~,fnameonly,~] = fileparts(fname);
% 
% % save the image in jpg for direct viewing
% load([path_to_file,fname])
% %imwrite(img_out,'../media/documents/jpg/image.jpg','jpg')
% imwrite(img_out,'/var/www/html/nm/image.jpg','jpg')  
% % delete all current file in working dir
% delete([working_dir,'imgs/*.mat'])
% 
% % copy file to MATLAB working dir
% copyfile([path_to_file,fname],[working_dir,'imgs'])

% run characterization algorithm
addpath('./descriptor_char'); % add path of directory holding MAIN.m
Descriptor_C2_Binary(path_to_write,input_type); %

% % move char results to another folder
% movefile([working_dir,'imgs/ch_result.mat'],'./char_result')



%% ZIP files %%
zip([path_to_write,'/Results.zip'],{'*'},path_to_write);

%% Email to user%%
To = ['To:',user_name];
Subject = ['Subject: Characterization complete for Job ID: ',Job_ID];
Content = 'Content-Type:text/html; charset="us-ascii"';
html_headers = '<html><body>';
%NM_logo = '<img src=''http://129.105.90.149/nm/NanoMine-logo.JPG''>';
Body1 = '<p>Greeting from NanoMine!</p>';
Body2 = '<p>You are receiving this email because you had submitted an image for characterization using Descriptor Method.';
Body3 = ['The characterization process is complete and you can view the results','<a href= http://nanomine.northwestern.edu:8000/descchar_view_Result.html?foo=',num2str(Job_ID),'&submit=Send> here</a></p>'];
Body4 = '<p>Best Wishes,</p>';
Body5 = '<p>NanoMine Team.</p>';
Footer1 = '<p>***DO NOT REPLY TO THIS EMAIL***</p>';
html_footer = '</body></html>';
Body = [Body2,Body3];

fileID = fopen('/home/NANOMINE/Production/mdcs/descchar/email.html','wt+');
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


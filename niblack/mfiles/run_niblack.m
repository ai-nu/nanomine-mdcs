function run_niblack(file_name)
% Run niblack algorithm 

% Get current adjust from user input
file=fopen('adjust.txt','r');
adjust=fscanf(file,['%u']);
fclose(file);

% default starting window size
%winsize = 60;
file=fopen('winsize','r');
winsize=fscanf(file,['%u']);
fclose(file);

c = clock; 
year = c(1); month = c(2); date = c(3);
if month < 10 % convert single digit to double
    str_month = ['0',num2str(month)];
else
    str_month = num2str(month);
end

if date < 10 % convert single digit to double
    str_date = ['0',num2str(date)];
else
    str_date = num2str(date);
end

path_to_file = ['../media/documents/',num2str(year),'/',str_month,'/',str_date,'/'];
working_dir = './niblack/';

disp(path_to_file)
% find all .mat files in today's upload
% f = dir([path_to_file,'*.tif']);
% disp([path_to_file,'*.tif'])
% nf = length(f)
% 
% for i = 1:nf
%     if i == 1
%         timestamp = f(i).datenum;
%         fid = i; 
%     elseif f(i).datenum > timestamp
%         timestamp = f(i).datenum;
%         fid = i;
%     end
% end
% 
% % filename of the most recently uploaded
% fname = f(fid).name; 
 [~,fnameonly,~] = fileparts(file_name);

% save the image in jpg for direct viewing
img_in = imread([path_to_file,file_name]);
if size(img_in,3) > 3
    img_in = img_in(:,:,1:3);
end
imwrite(img_in,'../media/documents/jpg/NBbefore.jpg')
disp([path_to_file,file_name])

% delete all current MAT files in working dir
delete([working_dir,'imgs/*.mat'])

% copy file to MATLAB working dir
copyfile([path_to_file,file_name],[working_dir,'imgs'])

% run characterization algorithm
%run  ./myproject/mfiles/niblack/runniblack.m
addpath('./niblack/')

% Prompt user to input adjust value from web page
runniblack(file_name, winsize, adjust)

load_file =[working_dir,'imgs/',fnameonly,'.mat'];
load(load_file)
imwrite(img_th,'../media/documents/jpg/NBafter.jpg','jpg')

% move char results to another folder
movefile(load_file,'./niblack_result')
end

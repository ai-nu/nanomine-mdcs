function runniblack(file_name, win0, adjust)

filepath = './niblack/imgs/';
img_path = strcat(filepath,file_name);
flag = 0;
win = win0;

%cut_side = 5; 
filter_r = 10;

img = imread(img_path); % read file
img = img(:,:,1); %get 2D image
pixel_size = min(size(img));
img_size = pixel_size;
%img = img (1:pixel_size, 1:pixel_size);
%GBbr = 5; % filter size
%GBbs = 1; % standard deviation
%G = fspecial('gaussian',GBbr,GBbs);
%img_blurred = imfilter(img,G,'same');
img_blurred = medfilt2(img, [filter_r filter_r]);
%img_blurred = img_blurred((1+cut_side):(pixel_size-cut_side), (1+cut_side):(pixel_size-cut_side));
if adjust > 0 
    win = adjust;
end
img_th = niblack(img_blurred, [win, win], -.2,10);
img_th = imcomplement(img_th);
%remove white edges: right and bottom
img_th(:,size(img,2))=0;
img_th(size(img,1),:)=0;
img_th = noise_filter(img_th);

%img1 = img_out;
%[img_out, VF] = black_dot(img_out);
[~,fnameonly,~] = fileparts(file_name);
save_path = strcat(filepath,fnameonly,'.mat');
save(save_path,'img_th');
VF = round(100*mean(img_th(:)),3); % vf for white phase,
fname = file_name;
win_size = win;

% Save summary result into MAT file for views to read
save([filepath,'NiblackSummary.mat'], 'fname', 'win_size','img_size','adjust','VF');
end

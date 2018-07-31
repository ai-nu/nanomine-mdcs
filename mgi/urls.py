################################################################################
#
# File Name: urls.py
# Application: mgi
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'mgi.views.home', name='home'),
    url(r'^admin/', include('admin_mdcs.urls')),
    url(r'^curate/', include('curate.urls')),
    url(r'^explore/', include('explore.urls')),
    url(r'^compose/', include('compose.urls')),
    
    # naonomine
    url(r'^FEA2D/', include('FEA2D.urls')),
    url(r'^MCFEA/', include('MCFEA.urls')),
    # Binarization
    url(r'^Binarization_Choice/','Otsu.views.Binarization_Choice',name='Binarization_Choice'),
    url(r'^Otsu/','Otsu.views.Binarize_Otsu',name='Otsu_Image_Submission'),
    url(r'^Otsu_Check_Result','Otsu.views.checkResult',name='Otsu_checkResult'),
    url(r'^Otsu_view_Result','Otsu.views.viewResult',name='Otsu_view_Result'),
    url(r'^Otsu_submission_notify','Otsu.views.submission_notify',name='Otsu_submission_notify'),
    url(r'^niblack/','niblack.views.home',name='niblack'),
    url(r'^niblack_view$','niblack.views.check',name='niblack-check'),    

    # SDF
    url(r'^SDFchar/', 'SDF.views.Characterize',name='SDFchar_Image_Submission'),
    url(r'^SDF_submision_notify', 'SDF.views.submission_notify',name='SDF_submission_notify'),
    url(r'^SDFchar_view_Result', 'SDF.views.viewResultChar',name='SDFchar_view_Result'),
    url(r'^SDFrecon/', 'SDF.views.Reconstruct',name='SDFrecon_Image_Submission'),
    url(r'^SDFrecon_view_Result', 'SDF.views.viewResultRecon',name='SDFrecon_view_Result'),

    # Descriptor characterization/reconstruction
    url(r'^descchar/', 'descchar.views.home',name='descchar_Image_Submission'),
    url(r'^descchar_submision_notify', 'descchar.views.submission_notify',name='descchar_submission_notify'),
    url(r'^descchar_view_Result', 'descchar.views.viewResult',name='descchar_view_Result'),
    url(r'^descchar_Results_interpretation','descchar.views.Results_interpretation',name='descchar_Results_interpretation'),
    url(r'^RECON/', 'RECON.views.Reconstruct', name='RECON_Image_Submission'),
    url(r'^RECON_submission_notify', 'RECON.views.submission_notify',name='RECON_submission_notify'),
    url(r'^RECON_view_Result', 'RECON.views.viewResultRecon',name='RECON_view_Result'),
    
    url(r'^stats_tool/', 'mgi.views.stats_tool', name='stats_tool'),
    url(r'^simulate_tool/', 'mgi.views.simulate_tool', name='simulate_tool'),
    #url(r'^dynamfit/', include('Dynamfit.urls')),
    url(r'^dynamfit/', 'Dynamfit.views.home', name='dynamfit'),
    url(r'^DynamfitRun$', 'Dynamfit.views.runmodel', name='dynamfit_runmodel'),
    url(r'^DynamfitExample$', 'Dynamfit.views.sample', name='dynamfit_sample'),
    url(r'^DynamfitExampleInput$', 'Dynamfit.views.sampleinput', name='dynamfit_sampleinput'),
    url(r'^DynamfitExampleRun$', 'Dynamfit.views.samplerun', name='dynamfit_samplerun'),
    #url(r'^AUTOFIT/', include('AUTOFIT.urls')),
    url(r'^AUTOFIT/', 'AUTOFIT.views.home', name='AUTOFIT'),
    url(r'^AUTOFITRun$', 'AUTOFIT.views.runmodel', name='AUTOFIT_runmodel'),
    url(r'^AUTOFITCheck$', 'AUTOFIT.views.check', name='AUTOFIT_check'),
    url(r'^AUTOFITSample$', 'AUTOFIT.views.sample', name='AUTOFIT.sample'),
    url(r'^XMLCONV/', 'XMLCONV.views.home', name='XMLCONV'),
    url(r'^Two_pt_MCR/','Two_pt_MCR.views.landing',name='Two_pt_MCR'),
    url(r'^Two_pt_MCR_Image_Submission','Two_pt_MCR.views.submit_image',name='Two_pt_MCR_Image_Submission'),
    url(r'^Two_pt_MCR_view_result','Two_pt_MCR.views.viewResult',name='Two_pt_MCR_view_result'),
    url(r'^Two_pt_MCR_submission_notify','Two_pt_MCR.views.submission_notify',name='Two_pt_MCR_submission_notify'),
    url(r'^Two_pt_MCR_Characterize','Two_pt_MCR.views.Characterize',name='Two_pt_MCR_Characterize'),
    url(r'^Two_pt_MCR_time_estimate','Two_pt_MCR.views.time_estimate',name='Two_pt_MCR_time_estimate'),
    url(r'^MCR_Characterize_Choice','Two_pt_MCR.views.Characterize_Choice',name='Characterize_Choice'),
    url(r'^MCR_Characterize_view_result','Two_pt_MCR.views.Characterize_view_result',name='Characterize_view_result'),
    url(r'^MCR_Reconstruction_Choice','Two_pt_MCR.views.Reconstruction_Choice',name='Reconstruction_Choice'),
    url(r'^MCR_Correlation_Fundamentals','Two_pt_MCR.views.Correlation_Fundamentals',name='Correlation_Fundamentals'),
    url(r'^MCR_Results_interpretation','Two_pt_MCR.views.Result_interpretation',name='Results_interpretation'),
    url(r'^SDF_Characterize','Two_pt_MCR.views.SDF',name='SDF_Characterize'),
    url(r'^SDF_Reconstruction','Two_pt_MCR.views.SDF',name='SDF_Reconstruction'),
    # search
    url(r'^search/', 'search.views.index', name='search'),
    url(r'^notify/', 'mgi.views.notify', name='notify'),
    ###    
    
    url(r'^rest/', include('api.urls')),
    url(r'^modules/', include('modules.urls')),
    url(r'^docs/api', include('rest_framework_swagger.urls')),
    url(r'^all-options', 'mgi.views.all_options', name='all-options'),
    url(r'^browse-all', 'mgi.views.browse_all', name='browse-all'),
    url(r'^login', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    url(r'^request-new-account', 'mgi.views.request_new_account', name='request-new-account'),   
    url(r'^logout', 'mgi.views.logout_view', name='logout'),
    url(r'^my-profile$', 'mgi.views.my_profile', name='my-profile'),
    url(r'^my-profile/edit', 'mgi.views.my_profile_edit', name='my-profile-edit'),
    url(r'^my-profile/change-password', 'mgi.views.my_profile_change_password', name='my-profile-change-password'),
    url(r'^my-profile/my-forms', 'mgi.views.my_profile_my_forms', name='my-profile-my-forms'),
    url(r'^my-profile/resources$', 'mgi.views.my_profile_resources', name='my-profile-resources'),
    url(r'^help', 'mgi.views.help', name='help'),
    url(r'^contact', 'mgi.views.contact', name='contact'),
    url(r'^privacy-policy', 'mgi.views.privacy_policy', name='privacy-policy'),
    url(r'^terms-of-use', 'mgi.views.terms_of_use', name='terms-of-use'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^dashboard$', 'mgi.views.dashboard', name='dashboard'),
)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += staticfiles_urlpatterns()




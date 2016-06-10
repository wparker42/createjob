templatepathdict = {
    1:('Civil', r'\\bldr-civil1\bldr_civil\CIVIL\NJFT\_NJFT'),
    2:('Environmental', r'\\bldr-civil1\Bldr_Civil\CIVIL\Environmental\2015 Efficiency - Team 5\Standard Job Folder Organization\9999c'),
    3:('Structural', r'\\bldr-struct1\bldr_structural\_proposed folder tree'),
    # Remove after testing
    4:('testing', r'\\JTIME1\den-civ\_create job folder [TESTING]\Test Master Template Folder')
}

serverlistdict = {
    1: [
        'Denver (Q:\)',
        'Boulder (J:\)',
        'Fort Collins (V:\)', 
        'Winter Park (K:\)',
        # Remove after testing
        'Desktop (C:\)'
    ],
    2: [
        'Denver (Q:\)',
        'Boulder (J:\)',
        'Fort Collins (V:\)', 
        'Winter Park (K:\)'
    ],
    3: [
        'Boulder (Z:\)',
        'Fort Collins (Y:\)',
        'Winter Park (X:\)'
    ],
    # Remove after testing
    4: [
        'Desktop (C:\)'
    ]
}

serverpathdict = {
    'Denver (Q:\)': r'\\JTIME1\den-civ',
    'Boulder (J:\)': r'\\bldr-civil1\bldr_civil',
    'Fort Collins (V:\)': r'\\server-fc\FC-Civil-Jobs',
    'Winter Park (K:\)': r'\\SERVER-WP-NEW\WP-Civil-Jobs',
    'Desktop (C:\)': r'C:\Users\WTP\Desktop',
    'Boulder (Z:\)': r'\\BLDR-STRUCT1\bldr_structural',
    'Fort Collins (Y:\)': r'\\server-fc\0jobs',
    'Winter Park (X:\)': r'\\server-wp-new\WP-Jobs'
}
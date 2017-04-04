from ftplib import FTP
import socket
import os

def configure():

    result = {}
    
    #This is the official OS FTP website
    result['host'] = 'ftp.os.uk'
    
    #DCS000... is the folder which we have in our FTP; this could be
    #different for different users.
    result['ftp_dir'] = '../from-os/DCS0002464055'
    
    #Choosing to download the data in a temporary directory
    result['download_dir'] = "C:\\TEMP"

    #I have stored our FTP credentials in the system's environment
    #For other users this could be hardcoded or read from a file,
    #database and so on.
    result['username'] = os.getenv('osma_ftp_user')
    result['password'] = os.getenv('osma_ftp_pass')

    return result

def host_to_ip(host):
    '''(str) -> str
    Returns the public IP address for a host
    >>>host_to_ip(ftp.os.uk)
    62.255.172.77
    >>>host_to_ip(www.google.com)
    216.58.198.228
    '''

    return socket.gethostbyname('ftp.os.uk')

def ftp_connection(ip,username,password):
    '''(str,str,str) -> object
    Returns an authentication FTP connection object
    with a memory address
    >>>ftp_connection('62.255.172.77','john_doe','password')
    object
    '''
    
    ftp = FTP(ip)
    ftp.login(username,password)

    return ftp

def get_filenames(ftp_connection,data_dir):
    '''(str) -> list
    Returns a list with the AddressBase files which
    will be downloaded.
    >>>get_filenames(object,'../from-os/DCS0002464055')
    ['AddressBasePremium_FULL_2017-03-23_001_csv.zip',\
    'AddressBasePremium_FULL_2017-03-23_002_csv.zip']
    '''
    
    #Change working directory to where the files for Address Base are located
    ftp_connection.cwd(data_dir)
    
    #Return a list of files within the working directory
    files = ftp_connection.nlst()

    #Appends to a list the filename if the string 'Address' is part of the filename.
    #To avoid downloading files which are not Address Base Premium related.
    return filter(lambda x: 'Address' in x,files)

def download_files(ftp_connection,filenames,download_dir):
    '''(object,list,str) -> None
    Returns None & downloads all the files for AddressBase
    Premium in the download directory set in configure()
    '''

    for filename in filenames:
        
        download_file = 'RETR {0}'.format(filename)
        write_file = '{0}\\{1}'.format(download_dir,filename)
        
        ftp_connection.retrbinary(download_file,open(write_file,'wb').write)
    
    return None

def main():

    #Collect objects & credentials which will be used in this script
    Configuration = configure()

    #Will be using the ftplib python module to download files
    #which requires an IP (e.g. 62.255.172.77) instead of a host
    #name(e.g. ftp.os.uk).
    IP = host_to_ip(Configuration.get('host'))

    #Connect to the IP using ftplib and authenticate the connection
    #using the OS credentials provided.
    FTPConnection = ftp_connection(IP,\
                                   Configuration.get('username'),\
                                   Configuration.get('password'),\
                                   )
    
    #Collect all the filenames which will be downloaded from the directory
    #of interest and store them in a list
    FileNames = get_filenames(FTPConnection,\
                              Configuration.get('ftp_dir')\
                              )
    
    #Download the files using the collected filenames and store them
    #into the download directory
    download_files(FTPConnection,\
                   FileNames,\
                   Configuration.get('download_dir')\
                   )

    #Close the FTP connection
    FTPConnection.quit()
    
if __name__ == "__main__":
    main()

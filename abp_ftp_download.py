from ftplib import FTP
import socket
import os

def configure():

    result = {}

    result['host'] = 'ftp.os.uk'
    result['ftp_dir'] = '../from-os/DCS0002464055'
    result['download_dir'] = "C:\\TEMP"

    #I have stored our FTP credentials in the system's environment
    result['username'] = os.getenv('osma_ftp_user')
    result['password'] = os.getenv('osma_ftp_pass')

    return result

def host_to_ip(host):
    '''(str) -> str
    Returns the public IP address for a host
    '''

    return socket.gethostbyname('ftp.os.uk')

def ftp_connection(ip,username,password):
    '''
    Returns an authentication FTP connection object
    with a memory address
    '''
    
    ftp = FTP(ip)
    ftp.login(username,password)

    return ftp

def get_filenames(ftp_connection,data_dir):
    '''(str) -> list
    Returns a list with the AddressBase files which
    will be downloaded
    '''

    ftp_connection.cwd(data_dir)
    files = ftp_connection.nlst()

    return filter(lambda x: 'Address' in x,files)

def download_files(ftp_connection,filenames,download_dir):
    '''
    Returns None & downloads all the files for AddressBase
    Premium in the download directory set in configure()
    '''

    for filename in filenames:
        ftp_connection.retrbinary('RETR {0}'.format(filename),\
                                  open('{0}\\{1}'.format(download_dir,filename),'wb').write\
                                  )
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
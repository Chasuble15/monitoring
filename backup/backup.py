import shutil
import os
import datetime
import tarfile

# Obtenir la date du jour
today_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Création du chemin de destination
save_folder_path = os.path.join('/mnt/local_share', 'save_{}'.format(today_date))

# Liste des chemins à sauvegarder
prometheus_data_path = os.path.join('/var/lib/docker/volumes', 'energyaim_prometheus_data')
grafana_data_path = os.path.join('/var/lib/docker/volumes', 'energyaim_grafana_data')
victoria_data_path = os.path.join('/var/lib/docker/volumes', 'energyaim_victoriametrics')

# Copie des chemins à sauvegarder vers la destination
# shutil.copytree(prometheus_data_path, os.path.join(save_folder_path, 'energyaim_prometheus_data'))
# shutil.copytree(grafana_data_path, os.path.join(save_folder_path, 'energyaim_grafana_data'))

# Création de l'archive
name_of_file= os.path.join('/mnt/local_share', 'save_{}.tar'.format(today_date))

# Opening the file in write mode
file= tarfile.open(name_of_file, "w")

# Adding the folder to the tar file
file.add(prometheus_data_path)
file.add(grafana_data_path)
file.add(victoria_data_path)

# Closing the file
file.close()

# Obtenir la liste des fichiers
files = os.listdir("/mnt/local_share")

# Obtenir la liste des éléments à supprimer (relativement à la date du jour)
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
delete_before = int(yesterday.strftime("%Y%m%d"))
print("Delete before :", delete_before)

# Suppression des fichiers choisis
for file in files:
    
    if int(file[5:-7]) < delete_before:
        shutil.rmtree(os.path.join("/mnt/local_share", file))
    




import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Application, ContextTypes

from aiogram import Bot, Dispatcher, types ,executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup

import requests


# Importer le module random
import random


def incrementer_nb(chaine):
  fichier= "utilisateurs.txt"
  # Ouvrir le fichier en mode lecture et écriture
  with open(fichier, "r+") as f:
    # Lire toutes les lignes du fichier dans une liste
    lignes = f.readlines()
    # Aller au début du fichier
    f.seek(0)
    # Parcourir chaque ligne
    for ligne in lignes:
      # Extraire le nom, l'id et le nb de la ligne
      nom, id, usr,nb = ligne.split(":")
      # Comparer l'id avec la chaîne
      if id.strip() == chaine:
        # Incrémenter le nb de 1
        nb = int(nb) + 1
        # Formater la nouvelle ligne avec le nb mis à jour
        nouvelle_ligne = f"{nom}:{id}:{usr}:{nb}\n"
        # Ecrire la nouvelle ligne dans le fichier
        f.write(nouvelle_ligne)
      else:
        # Ecrire la ligne inchangée dans le fichier
        f.write(ligne)
    # Tronquer le fichier à la position actuelle
    f.truncate()

# Définition de la fonction genererChaine
def genererChaine():
  # Initialiser une liste vide pour stocker les caractères
  caracteres = []
  # Générer 5 chiffres aléatoires entre 0 et 9 et les ajouter à la liste
  for i in range(5):
    chiffre = random.randint(0, 9)
    caracteres.append(str(chiffre))
  # Générer 5 lettres aléatoires entre A et Z et les ajouter à la liste
  for i in range(5):
    lettre = chr(random.randint(65, 90))
    caracteres.append(lettre)
  # Mélanger la liste de caractères
  random.shuffle(caracteres)
  # Convertir la liste en une chaîne et la retourner
  chaine = "".join(caracteres)
  return chaine


# Définition de la fonction mettreInfo
def mettreInfo(chaine):
  # Ouvrir le fichier info.txt en mode lecture et écriture
  fichier = open("info.txt", "r+")
  # Lire le contenu du fichier et le stocker dans une liste de lignes
  lignes = fichier.readlines()
  # Fermer le fichier
  fichier.close()
  # Extraire partie1 et partie2 de la chaîne
  partie1, partie2 = chaine.split(":")
  # Initialiser un booléen pour indiquer si partie1 a été trouvée
  trouve = False
  # Parcourir la liste des lignes
  for i in range(len(lignes)):
    # Si la ligne commence par partie1, la remplacer par la chaîne
    if lignes[i].startswith(partie1):
      lignes[i] = chaine + "\n"
      trouve = True
      break
  # Si partie1 n'a pas été trouvée, ajouter la chaîne à la fin de la liste
  if not trouve:
    lignes.append(chaine + "\n")
  # Ouvrir le fichier info.txt en mode écriture
  fichier = open("info.txt", "w")
  # Écrire la liste des lignes dans le fichier
  fichier.writelines(lignes)
  # Fermer le fichier
  fichier.close()

# Définition de la fonction getInfo
def getInfo(partie1):
  # Ouvrir le fichier info.txt en mode lecture
  fichier = open("info.txt", "r")
  # Lire le contenu du fichier et le stocker dans une liste de lignes
  lignes = fichier.readlines()
  # Fermer le fichier
  fichier.close()
  # Parcourir la liste des lignes
  for ligne in lignes:
    # Si la ligne commence par partie1, extraire et retourner partie2
    if ligne.startswith(partie1):
      partie2 = ligne.split(":",1)[1].strip()
      return partie2
  # Si partie1 n'a pas été trouvée, retourner None
  return None




def recuperer_noms():
  fichier= "utilisateurs.txt"
  # Créer une chaîne vide pour stocker les noms
  chaine_noms = ""
  # Ouvrir le fichier en mode lecture
  with open(fichier, "r") as f:
    # Lire toutes les lignes du fichier
    lignes = f.readlines()
    # Parcourir chaque ligne
    for ligne in lignes:
      # Extraire le nom de la ligne
      nom = ligne.split(":")[0].strip()+" : "+ligne.split(":")[2].strip()
      # Ajouter le nom à la chaîne avec deux sauts de ligne
      chaine_noms += nom + " \n \n"
  # Retourner la chaîne des noms
  return "LISTE DES MEMBRES :  \n \n" + chaine_noms

def enregistrer_id(id, nom,username):
  fichier= "utilisateurs.txt"
  # Ouvrir le fichier en mode lecture et écriture, ou le créer s'il n'existe pas
  with open(fichier, "a+") as f:
    # Aller au début du fichier
    f.seek(0)
    # Lire toutes les lignes du fichier dans une liste
    lignes = f.readlines()
    # Vérifier si l'id existe déjà dans le fichier
    existe = False
    for ligne in lignes:
      # Extraire l'id de la ligne
      id_ligne = ligne.split(":")[1].strip()
      # Comparer l'id avec celui passé en paramètre
      if id_ligne == id:
        # L'id existe déjà, on met le drapeau à True
        existe = True
        break
    # Si l'id n'existe pas, on l'ajoute à la fin du fichier avec le nom
    if not existe:
      # Formater la ligne à écrire
      ligne = f"{nom}:{id}:{username} \n"
      # Ecrire la ligne dans le fichier
      f.write(ligne)

def recuperer_id():
  fichier= "utilisateurs.txt"
  # Créer une liste vide pour stocker les id
  liste_id = []
  # Ouvrir le fichier en mode lecture
  with open(fichier, "r") as f:
    # Lire toutes les lignes du fichier
    lignes = f.readlines()
    # Parcourir chaque ligne
    for ligne in lignes:
      # Extraire l'id de la ligne
      id = ligne.split(":")[1].strip()
      # Convertir l'id en entier
      id = int(id)
      # Ajouter l'id à la liste
      liste_id.append(id)
  # Retourner la liste des id
  return liste_id

def recuperer_idPersonnne(nom):
  fichier="utilisateurs.txt"
  # Ouvrir le fichier en mode lecture
  with open(fichier, "r") as f:
    # Lire toutes les lignes du fichier
    lignes = f.readlines()
    # Parcourir chaque ligne
    for ligne in lignes:
      # Extraire le nom et l'id de la ligne
      id_ligne = ligne.split(":")[1].strip()
      nom_ligne=ligne.split(":")[0].strip()
      # Comparer le nom avec celui passé en paramètre
      if nom_ligne.strip().__contains__(nom) :
        # Retourner l'id correspondant
        return id_ligne.strip()
    # Si le nom n'est pas trouvé, retourner None
    return None


def recuperer_nbPersonnne(ident):
  id=str(ident)
  fichier="utilisateurs.txt"
  # Ouvrir le fichier en mode lecture
  with open(fichier, "r") as f:
    # Lire toutes les lignes du fichier
    lignes = f.readlines()
    # Parcourir chaque ligne
    for ligne in lignes:
      # Extraire le nom et l'id de la ligne
      id_ligne = ligne.split(":")[1].strip()
      nb_ligne=ligne.split(":")[3].strip()
      # Comparer le nom avec celui passé en paramètre
      if id_ligne.strip().__contains__(id) :
        # Retourner l'id correspondant
        return int(nb_ligne)
    # Si le nom n'est pas trouvé, retourner None
    return None



Token = '6654795724:AAGyIdjddrrkDh0L7HCjmmh1J6w9MugbiEc'
canal=getInfo("canal")
print(canal)
bot = Bot(token=Token)
dp = Dispatcher(bot)
#button1 = InlineKeyboardButton(text="Commencer", callback_data="In_First_button") 
button2 = InlineKeyboardButton(text="Notre canal officiel 🏆", url=canal) 
keyboard_inline = InlineKeyboardMarkup().add( button2) 



@dp.message_handler(commands=['start2']) 
async def check(message: types.Message): 
   await message.reply("hi! how are you", reply_markup=keyboard_inline)
   enregistrer_id(str(message.chat.id),message.from_user.full_name,"@"+ str( message.from_user.username))
   
        
@dp.message_handler(commands=['membres']) 
async def Membres(message: types.Message): 
  await bot.send_message(chat_id=message.chat.id,text=recuperer_noms())

@dp.callback_query_handler(text=["In_First_button", "In_Second_button"]) 
async def check_button(call: types.CallbackQuery): 
   if call.data == "In_First_button": 
       
       await call.message.reply_photo("https://sf.football.fr/wp-content/uploads/2024/02/Ethan-et-Kylian-Mbappe%CC%81-.jpg",caption="Merci de nous faire confiance  ")
   if call.data == "In_Second_button": 
    pass       
   await call.answer()
########################################################################################################################################################
##################################################################################################################################################################
# LES CLAVIERS DE REPONSES 
################################################################################################################################################################   
# Creating the reply keyboard 

async def proposer_clavier3(message: types.Message):
  # Créer un clavier avec les trois boutons et les emoji
  keyboard_reply3 = types.ReplyKeyboardMarkup(
    resize_keyboard=False, one_time_keyboard=False).add("1xbet 🟦📱", "Betwinner 🟩📱", "Melbet 🎲", "Retour Menu 📋")
  # Envoyer un message avec le clavier
  await message.answer("Choisissez une option parmi les suivantes :", reply_markup=keyboard_reply3)


async def proposer_clavier2(message: types.Message):
  # Créer un clavier avec les trois boutons et les emoji
  keyboard_reply2 = types.ReplyKeyboardMarkup(
    resize_keyboard=False, one_time_keyboard=False).add("C'est fait ✅", "Retour Menu 📋")
  # Envoyer un message avec le clavier
  await message.answer_photo(photo="https://sf.football.fr/wp-content/uploads/2024/02/Ethan-et-Kylian-Mbappe%CC%81-.jpg",caption=f"Ici vous allez recevoir les prédictions du jeux SWAMP LAND\n\n\
 \
\n🛑 Mais pour que les prédictions puis bien fonctionné, vous devez obligatoirement créer un nouveau compte 1xbet, MELBET ou betwinner avec le code promo : {getInfo('code')} ✅\n\n\
 \
 \
\n\nSi c \'est fait cliquez sur c \'est fait ✅", reply_markup=keyboard_reply2)  
  
async def proposer_clavier4(message: types.Message):
  # Créer un clavier avec les trois boutons et les emoji
  keyboard_reply4 = types.ReplyKeyboardMarkup(
    resize_keyboard=False, one_time_keyboard=False).add("Trouver la bonne case 🔍", "Retour Menu 📋")
  # Envoyer un message avec le clavier
  await message.answer_photo(photo="https://sf.football.fr/wp-content/uploads/2024/02/Ethan-et-Kylian-Mbappe%CC%81-.jpg",caption=f"À fin de recevoir les meilleurs production SWAMP LAND vous devez être inscrit obligatoirement avec le code promo : {getInfo('code')} \
 \
SI C \'EST FAIT ✅ \
cliquez sur 'trouver la bonne case' pour commencer les prédictions \
 \
👇👇👇👇👇👇", reply_markup=keyboard_reply4)  

async def proposer_clavier5(message: types.Message):
  # Créer un clavier avec les deux boutons
  keyboard_reply5 = types.ReplyKeyboardMarkup(
    resize_keyboard=False, one_time_keyboard=False).add("Soldes 💰", "Retirer 🏧")
  # Envoyer un message avec le clavier
  await message.answer("Choisissez une option parmi les suivantes :", reply_markup=keyboard_reply5)

keyboard_reply1 = types.ReplyKeyboardMarkup(
    resize_keyboard=False, one_time_keyboard=False).add("📱Coupon du jour🔥", "DE PRÉDICTION 🎲", "⚽COUPON VIP⚽", "Comment ça marche❗", "Canal officiel⚜️", "1000 FCFA à gagner💰")
########################################################################################################################################################
##################################################################################################################################################################
# LES CLAVIERS DE REPONSES 
################################################################################################################################################################  


# Handling the /start and /help commands
########################################################################################################################################################
##################################################################################################################################################################
# LES FONCTIONS DE REPONSES CLAVIER
################################################################################################################################################################  

 
@dp.message_handler(commands=['start', 'menu']) 
async def welcome(message: types.Message):
   
    print(message.get_args())
    if message.get_args():
      if str(message.get_args())!=str(message.from_user.id):
        incrementer_nb(str(message.get_args()))
    # Sending a greeting message that includes the reply keyboard 
    await message.answer_photo(photo="https://www.237online.com/wp-content/uploads/2022/02/Coupe-du-monde-avec-1xbet-900x500.jpg",caption="Bonjour , Bienvenue dans notre Bot que pouvons-nous faire pour vous ?",reply_markup=keyboard_reply1)

    #await message.reply("Choisissez une proposition", reply_markup=keyboard_inline)
    enregistrer_id(str(message.chat.id),message.from_user.full_name,"@"+ str( message.from_user.username))
   

   

########################################################################################################################################################
##################################################################################################################################################################
# LES FONCTIONS DE REPONSES CLAVIER
################################################################################################################################################################  

   
# Handling all other messages 
@dp.message_handler() 
async def check_rp(message: types.Message): 

    if message.text == "📱Coupon du jour🔥": 
        # Responding with a message for the first button 
        await message.reply(f"Veiller vous inscrire sur 1xbet, betwinner, melbet et 888 STARZ avec le code promo : \n \n{getInfo('code2')} OU \n \n{getInfo('code')} ✅ \n \n \nLIEN D'INSCRIPTION \n \n\n➡️ Lien d'inscription 1xbet🟦 \nhttps://affpa.top/L?tag=d_1685907m_97c_&site=1685907&ad=97 \n \n\n➡️ Lien d'inscription BETWINNER 🟩 \n \nhttps://bwredir.com/1M7s \n \n\n➡️ Lien d'inscription melbet \n \nhttps://bit.ly/3PzV5WK \n \n\n➡️ Lien d'inscription 888starz 🔴 \n \nhttps://yourbonus.online/L?tag=d_2759153m_37513c_&site=2759153&ad=37513 \n \n \n\n➡️ Lien d'inscription BET AND YOU 📱 \nhttps://refpacd.top//L?tag=d_2778453m_63039c_&site=2778453&ad=63039") 
        await proposer_clavier3(message=message)
    elif message.text == "DE PRÉDICTION 🎲": 
        # Responding with a message for the second button
        await proposer_clavier2(message=message) 
    elif message.text== "⚽COUPON VIP⚽":
        await message.reply_photo("https://www.africatopsports.com/wp-content/uploads/2020/04/1xbet-bonuses-710x394.jpg",caption=f"Pour avoir accès à notre VIP veillez vous inscrire en utilisant le code promo {getInfo('code')}\nVoici les bookmakers où vous pouvez le code promo {getInfo('code')} sur 1xbet, betwinner et melbet\nAprès votre inscription veiller envoyer les captures d'écran qui montre que vous avez utilisé le code promo {getInfo('code')}")
 
    elif message.text== "Comment ça marche❗":
        await message.reply(f"✅1xbet pronos: \nCette option est disponible uniquement pour ceux qui veulent créer un nouveau compte 1xbet \n \n\n➡️Donc veuillez créer un nouveau compte en utilisant le code promo ✅ {getInfo('code')} OU {getInfo('code2')} ✅ \n \n\n➡️Ensuite faites une capture d’écran et envoyez-la ici \n \n🔴NB: toute personne qui va envoyer une fausse capture d’écran sera renvoyée du bot \n \nEnvoyez la capture d’écran ici 👇 \n \n\n➡️Pour avoir accès au coupon gratuit vous devez obligatoirement créer un nouveau compte 1xbet en utilisant notre code promo : ✅  \n{getInfo('code')} OU {getInfo('code2')} ✅ \n \n\n➡️Ensuite vous devez faire votre premier dépôt pour commencer à gagner avec mes coupons gratuits  \n \n✅✅Gagnez 100% de vos paris avec mes coupons gratuits")

   
    elif message.text== "Canal officiel⚜️":
        # Sending a greeting message that includes the reply keyboard 
        await message.reply("Vous devez obligatoirement rejoindre notre canal officiel", reply_markup=keyboard_inline)
   
    elif message.text== "1000 FCFA à gagner💰":
       # Créer un clavier avec les deux boutons
        keyboard_reply5 = types.ReplyKeyboardMarkup(
          resize_keyboard=False, one_time_keyboard=False).add("Soldes 💰", "Retirer 🏧")
        # Envoyer un message avec le clavier
        await message.answer(f"Vous avez la possibilité de gagner 100k fcfa en invitant plus de monde a rejoindre la bot\n \
 \
Voici votre lien de parrainage:\n\n\
{getInfo('lien')}?start={message.from_user.id}\n\n\
 \
Vous avez {recuperer_nbPersonnne(message.from_user.id)} membres dans votre équipe\n\n\
 \
Pour chaque personne invité vous recevrez 1000f\n\n\
 \
Dès que vous atteignez 100k FCFA, \
 \
Cliquez sur:\n\
recuperer le cheick✅",reply_markup=keyboard_reply5)
    elif message.text=="1xbet 🟦📱":
        await message.answer(f"Cette option est disponible uniquement pour ceux qui veulent créer un nouveau compte **1XBET** \n \n\n➡️Donc veuillez créer un nouveau compte en utilisant le code promo ** {getInfo('code2')} OU {getInfo('code')} ** \n \n\n➡️Ensuite faites une capture d’écran et envoyez-la ici \n \n🔴NB: toute personne qui va envoyer une fausse capture d’écran sera renvoyée du bot \n \nEnvoyez la capture d’écran ici 👇")
    elif message.text=="Betwinner 🟩📱":
        await message.answer(f"Cette option est disponible uniquement pour ceux qui veulent créer un nouveau compte **BETWINNER** \n \n\n➡️Donc veuillez créer un nouveau compte en utilisant le code promo ** {getInfo('code2')} OU {getInfo('code')} ** \n \n\n➡️Ensuite faites une capture d’écran et envoyez-la ici \n \n🔴NB: toute personne qui va envoyer une fausse capture d’écran sera renvoyée du bot \n \nEnvoyez la capture d’écran ici 👇")
    elif message.text=="Melbet 🎲":
        await message.answer(f"Cette option est disponible uniquement pour ceux qui veulent créer un nouveau compte **MELBET** \n \n\n➡️Donc veuillez créer un nouveau compte en utilisant le code promo ** {getInfo('code2')} OU {getInfo('code')} ** \n \n\n➡️Ensuite faites une capture d’écran et envoyez-la ici \n \n🔴NB: toute personne qui va envoyer une fausse capture d’écran sera renvoyée du bot \n \nEnvoyez la capture d’écran ici 👇")
    
    elif message.text=="menu":
        await message.answer("Que pouvons-nous faire pour vous ?", reply_markup=keyboard_reply1) 
    elif message.text=="Retour Menu 📋":
        await message.answer("Que pouvons-nous faire pour vous ?", reply_markup=keyboard_reply1) 
    elif message.text=="C'est fait ✅": 
          # Créer un clavier avec les trois boutons et les emoji
        keyboard_reply4 = types.ReplyKeyboardMarkup(
        resize_keyboard=False, one_time_keyboard=False).add("Trouver la bonne case 🔍", "Retour Menu 📋")
  # Envoyer un message avec le clavier
        await message.answer(f"À fin de recevoir les meilleurs production SWAMP LAND vous devez être inscrit obligatoirement avec le code promo : {getInfo('code')} \n \nSI C'EST FAIT ✅ \n \ncliquez sur trouver la bonne case pour commencer les prédictions", reply_markup=keyboard_reply4) 
    elif message.text=="Trouver la bonne case 🔍": 
        await message.answer(f"Veuilliez choisir la case {random.randint(1,5)}") 
    elif message.text=="Soldes 💰": 
        await message.reply(f"👋 Cher {message.from_user.full_name} \
\n➡️Votre solde est de {recuperer_nbPersonnne(message.from_user.id)*1000} FCFA💰\n\n\
\n➡️Vous avez invité au total {recuperer_nbPersonnne(message.from_user.id)} membres dans votre équipe👥\n \
 \
\n➡️Voici votre lien de parrainage \n\n\
{getInfo('lien')}?start={message.from_user.id}\n\n\
\n➡️Gagner 1000 FCFA pour chaque personne invité\n\nRetrait minimum 30000 FCFA") 
    elif message.text=="Retirer 🏧": 
          await message.reply(f"👋 Cher {message.from_user.full_name} \
\n➡️Votre solde est de {recuperer_nbPersonnne(message.from_user.id)*1000} FCFA💰\n\n\
\n➡️Vous avez invité au total {recuperer_nbPersonnne(message.from_user.id)} membres dans votre équipe👥\n \
\n➡️Voici votre lien de parrainage \n \
{getInfo('lien')}?start={message.from_user.id}\n \
\n➡️Gagner 1000 FCFA pour chaque personne invité\n \
Retrait minimum 30000 FCFA")
    elif message.text.startswith("code:") or message.text.startswith("canal:") or message.text.startswith("code2:"):
      mettreInfo(message.text) 
      await message.reply(f"Nous avons changé l'information  '{message.text}'") 

      
    
          
    

@dp.message_handler(content_types=types.ContentType.PHOTO) 
async def check_Photo(message: types.Message): 
    
    if message.caption.__contains__("🔥🔥"): 
        # Responding with a message that includes the text of the user's message 
        liste=recuperer_id()
        messageDeroupe=message.caption[8::1]
        print(messageDeroupe)
        message.caption=messageDeroupe
        
        for id in liste :
          await bot.forward_message(chat_id=id, message_id=message.message_id,from_chat_id= message.chat.id)
    elif message.photo:
        await message.reply("Votre image sera envoyee a l'administrateur")
        await bot.forward_message(chat_id=recuperer_idPersonnne("Gates Tem"), message_id=message.message_id,from_chat_id= message.chat.id)
        


# Starting the bot 
executor.start_polling(dp)

executor.start_polling(dp)


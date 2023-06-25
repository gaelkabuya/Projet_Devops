from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder="templates")

# Données de test etudiants et cours de complément
etudiants = [
       {"id": 1,"PRENOM":"GAEL","NOM":"KABUYA","POSTNOM":"KAZADI","age":"30","Promotion":"M2", "genre":"M"},
       {"id": 2,"PRENOM":"SALUT","NOM":"SAMUEL","POSTNOM":"LUKENDO","age":"29","Promotion":"M2","genre":"M"},
       {"id": 3,"PRENOM":"LARRY","NOM":"KABALA","POSTNOM":"KILANGULA","age":"30","Promotion":"M2", "genre":"M"},
       {"id": 4,"PRENOM":"STEVE","NOM":"MIKOMBE","POSTNOM":"KABAMB","age":"29","Promotion":"M2","genre":"M"},
       {"id": 5,"PRENOM":"SHEKINA","NOM":"LUKWICH","POSTNOM":"KILANGULA","age":"30","Promotion":"M2", "genre":"M"},
       {"id": 6,"PRENOM":"MARIE","NOM":"KALENGA","POSTNOM":"ILUNGA","age":"29","Promotion":"M1","genre":"M"},
       {"id": 7,"PRENOM":"ERWIN","NOM":"KUMWIMBA","POSTNOM":"KUMWIMBA","age":"31","Promotion":"M1", "genre":"M"},
       {"id": 8,"PRENOM":"CAROLINE","NOM":"KALEYA","POSTNOM":"NGOIE","age":"29","Promotion":"M1","genre":"F"},
       {"id": 9,"PRENOM":"PRISCA","NOM":"KATANGA","POSTNOM":"MWEPU","age":"28","Promotion":"M1","genre":"F"},
       {"id": 10,"PRENOM":"LARISSA","NOM":"SOMPO","POSTNOM":"IRUNGA","age":"31","Promotion":"M2","genre":"F"}
]
cours = [
    {"id": 1,"etudiant_id": 4,"NOM":"Cloud_computing","Vol_Horaire":"75","credit":"5","Titulaire":"RYM","Promotion":"M2"},
    {"id": 2,"etudiant_id": 7,"NOM":"architecture reseaux","Vol_Horaire":"60","credit":"4","Titulaire":"JUSTICE","Promotion":"M1"},
    {"id": 3,"etudiant_id": 2,"NOM":"Electronique","Vol_Horaire":"45","credit":"3","Titulaire":"MONGA","Promotion":"M1"},
    {"id": 4,"etudiant_id": 2,"NOM":"Systeme optique","Vol_Horaire":"60","credit":"4","Titulaire":"MONGA","Promotion":"M1"},
    {"id": 5,"etudiant_id": 10,"NOM":"SUPERVISION","Vol_Horaire":"45","credit":"3","Titulaire":"DERICK","Promotion":"M2"},
    {"id": 6,"etudiant_id": 3,"NOM":"DEVNET","Vol_Horaire":"45","credit":"3","Titulaire":"PROF_BLAISE","Promotion":"M2"},
    {"id": 7,"etudiant_id": 9,"NOM":"ADMINISTRATION","Vol_Horaire":"75","credit":"5","Titulaire":"PATIENT","Promotion":"M2"},
    {"id": 8,"etudiant_id": 6,"NOM":"ANGLAIS","Vol_Horaire":"15","credit":"1","Titulaire":"PATRICK","Promotion":"M1"},
    {"id": 9,"etudiant_id": 8,"NOM":"SCRIPTS","Vol_Horaire":"45","credit":"3","Titulaire":"PROF_BLAISE","Promotion":"M2"},
    {"id": 10,"etudiant_id": 5,"NOM":"Systeme embarqué","Vol_Horaire":"45","credit":"3","Titulaire":"CHRISTIAN","Promotion":"M1"}
]    
    
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return: the rendered template 'home.html'
    """
    return render_template('page_accueil.html', etudiants=etudiants, cours=cours)

# Ressource pour obtenir tous les etudiants
@app.route('/etudiants', methods=['GET'])
def get_etudiants():
    return jsonify({'etudiants': etudiants})

# Ressource pour obtenir un etudiant spécifique
@app.route('/etudiants/<int:etudiant_id>', methods=['GET'])
def get_etudiant(etudiant_id):
    etudiant = next((etudiant for etudiant in etudiants if etudiant["id"] == etudiant_id), None)
    if etudiant is None:
        return jsonify({'erreur': 'etudiant introuvable'})
    else:
        return jsonify({'etudiant': etudiant})

# Ressource pour ajouter un etudiant
@app.route('/etudiants', methods=['POST'])
def create_etudiant():
    if not request.json or not 'NOM' in request.json:
        return jsonify({'erreur': 'mauvaise requette'})
    etudiant = {"id": len(etudiants) + 1, "NOM": request.json['NOM'], "POSTNOM": request.json['POSTNOM'],"PRENOM": request.json['PRENOM']}
    etudiants.append(etudiant)
    return jsonify({'message': 'Etudiant créé avec succès', 'etudiant': etudiant})


# Ressource pour obtenir tous les cours
@app.route('/cours', methods=['GET'])
def get_cours():
    return jsonify({'cours': cours})
# Ressource pour obtenir un cours spécifique
@app.route('/cours/<int:cour_id>', methods=['GET'])
def get_cour(cour_id):
    cour = next((cour for cour in cours if cour["id"] == cour_id), None)
    if cour is None:
        return jsonify({'erreur': 'cours introuvable'})
    else:
        return jsonify({'cour': cour})

# Ressource pour ajouter un cours
@app.route('/cours', methods=['POST'])
def create_cour():
    if not request.json or not 'NOM' in request.json or not 'etudiant_id' in request.json:
        return jsonify({'error': 'mauvaise requette'})
    etudiant_id = request.json['etudiant_id']
    etudiant = next((etudiant for etudiant in etudiants if etudiant["id"] == etudiant_id), None)
    if etudiant is None:
        return jsonify({'erreur': 'etudiant introuvable'})
    cour = {"id": len(cours) + 1, "NOM": request.json['NOM'], "etudiant_id": etudiant_id}
    cours.append(cour)
    return jsonify({'cour': 'cour créé avec succès', 'cour': cour})

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
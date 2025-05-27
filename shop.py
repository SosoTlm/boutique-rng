import customtkinter as ctk
from tkinter import messagebox, simpledialog
import random
import json
import os
from datetime import datetime
import threading
import time

# Configuration du thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class NotificationSystem:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.notification_frame = None
        
    def show_notification(self, message, type="info", duration=5000):
        """Affiche une notification personnalisée"""
        if self.notification_frame:
            self.notification_frame.destroy()
        
        # Couleurs selon le type
        colors = {
            "info": ("#3B8ED0", "#1F6AA5"),
            "success": ("#2ECC71", "#27AE60"),
            "warning": ("#F39C12", "#E67E22"),
            "error": ("#E74C3C", "#C0392B")
        }
        
        bg_color = colors.get(type, colors["info"])
        
        self.notification_frame = ctk.CTkFrame(
            self.parent.root,
            fg_color=bg_color,
            corner_radius=10,
            height=60
        )
        self.notification_frame.place(relx=0.5, rely=0.1, anchor="center")
        
        # Message
        msg_label = ctk.CTkLabel(
            self.notification_frame,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        msg_label.pack(pady=15, padx=20)
        
        # Bouton fermer
        close_btn = ctk.CTkButton(
            self.notification_frame,
            text="✕",
            width=30,
            height=30,
            command=self.close_notification,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        close_btn.place(relx=0.95, rely=0.5, anchor="center")
        
        # Auto-fermeture
        self.parent.root.after(duration, self.close_notification)
    
    def close_notification(self):
        if self.notification_frame:
            self.notification_frame.destroy()
            self.notification_frame = None

class BoutiqueShop:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Boutique Exclusive - Version Pro")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.resizable(True, True)
        
        # Système de notification
        self.notifications = NotificationSystem(self)
        
        # Variables du jeu
        self.ecus = 1000  # Démarrage avec plus d'écus pour tester
        self.ecus_banque = 0
        self.experience = 0
        self.niveau = 1
        self.inventaire = []
        self.historique_achats = []
        self.historique_ventes = []
        self.quetes = []
        
        # Articles de base
        self.articles = [
            {"nom": "Épée Légendaire", "prix": 150, "achats": 0, "description": "Une épée forgée par les dieux", "rareté": "Légendaire"},
            {"nom": "Armure Mystique", "prix": 200, "achats": 0, "description": "Protection magique ultime", "rareté": "Épique"},
            {"nom": "Potion Magique", "prix": 50, "achats": 0, "description": "Restaure toute votre énergie", "rareté": "Commun"},
            {"nom": "Bague de Pouvoir", "prix": 300, "achats": 0, "description": "Augmente tous vos sorts", "rareté": "Légendaire"},
            {"nom": "Bouclier Divin", "prix": 180, "achats": 0, "description": "Bloque toutes les attaques magiques", "rareté": "Épique"},
            {"nom": "Bottes de Vitesse", "prix": 120, "achats": 0, "description": "Triple votre vitesse de déplacement", "rareté": "Rare"},
            {"nom": "Grimoire Ancien", "prix": 250, "achats": 0, "description": "Contient les sorts les plus puissants", "rareté": "Légendaire"},
            {"nom": "Amulette de Chance", "prix": 90, "achats": 0, "description": "Augmente drastiquement votre chance", "rareté": "Rare"},
            {"nom": "Casque de Sagesse", "prix": 160, "achats": 0, "description": "Révèle les secrets cachés", "rareté": "Épique"},
            {"nom": "Gants de Force", "prix": 110, "achats": 0, "description": "Décuple votre force physique", "rareté": "Rare"},
            {"nom": "Cape d'Invisibilité", "prix": 400, "achats": 0, "description": "Vous rend complètement invisible", "rareté": "Mythique"},
            {"nom": "Cristal de Mana", "prix": 220, "achats": 0, "description": "Source inépuisable d'énergie magique", "rareté": "Épique"},
            {"nom": "Une Villa", "prix": 9347812, "achats": 0, "description": "Vous rend complètement invisible", "rareté": "Impossible"},
        ]
        
        # Initialiser les quêtes
        self.init_quetes()
        
        # Charger les données sauvegardées
        self.load_data()
        
        # Pages
        self.current_page = "boutique"
        self.setup_ui()
        
        # Message de bienvenue
        self.notifications.show_notification("🎉 Bienvenue dans la Boutique Exclusive !", "success")
    
    def init_quetes(self):
        self.quetes = [
            {"nom": "Premier Achat", "description": "Effectuez votre premier achat", "recompense": 50, "complete": False, "type": "achat", "objectif": 1},
            {"nom": "Collectionneur", "description": "Achetez 5 articles différents", "recompense": 200, "complete": False, "type": "achat", "objectif": 5},
            {"nom": "Marchand", "description": "Vendez 3 articles", "recompense": 100, "complete": False, "type": "vente", "objectif": 3},
            {"nom": "Épargnant", "description": "Économisez 1000 écus en banque", "recompense": 150, "complete": False, "type": "banque", "objectif": 1000},
            {"nom": "Aventurier Légendaire", "description": "Atteignez le niveau 5", "recompense": 500, "complete": False, "type": "niveau", "objectif": 5}
        ]
    
    def setup_ui(self):
        # Frame principal avec navigation
        self.nav_frame = ctk.CTkFrame(self.root, height=70, corner_radius=15)
        self.nav_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Boutons de navigation
        nav_buttons = [
            ("🏪 Boutique", "boutique"),
            ("💰 Banque", "banque"),
            ("🎒 Inventaire", "inventaire"),
            ("💼 Vendre", "vendre"),
            ("📊 Statistiques", "stats"),
            ("🎯 Quêtes", "quetes"),
            ("📈 Marché", "marche"),
            ("⚔️ Combat", "combat")
        ]
        
        self.nav_buttons = {}
        for i, (text, page) in enumerate(nav_buttons):
            btn = ctk.CTkButton(self.nav_frame, text=text, width=100, height=40,
                               corner_radius=10, command=lambda p=page: self.show_page(p))
            btn.pack(side="left", padx=5, pady=15)
            self.nav_buttons[page] = btn
        
        # Bouton pour ajouter un nouvel article
        add_button = ctk.CTkButton(self.nav_frame, text="➕ Ajouter", width=80, height=40,
                                  corner_radius=10, command=self.show_add_article_dialog)
        add_button.pack(side="left", padx=(10, 5), pady=15)
        
        # Informations du joueur
        info_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        info_frame.pack(side="right", padx=20)
        
        self.ecus_label = ctk.CTkLabel(info_frame, text=f"💰 {self.ecus}", 
                                      font=ctk.CTkFont(size=14, weight="bold"))
        self.ecus_label.pack(pady=2)
        
        self.level_label = ctk.CTkLabel(info_frame, text=f"⭐ Niveau {self.niveau} (XP: {self.experience})", 
                                       font=ctk.CTkFont(size=12))
        self.level_label.pack(pady=2)
        
        # Frame de contenu principal
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initialiser avec la page boutique
        self.show_page("boutique")
    
    def show_page(self, page):
        self.current_page = page
        
        # Nettoyer le contenu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mettre à jour les boutons de navigation
        for btn_page, btn in self.nav_buttons.items():
            if btn_page == page:
                btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                btn.configure(fg_color=("#1F6AA5", "#144870"))
        
        # Afficher la page correspondante
        if page == "boutique":
            self.show_boutique()
        elif page == "banque":
            self.show_banque()
        elif page == "inventaire":
            self.show_inventaire()
        elif page == "vendre":
            self.show_vendre()
        elif page == "stats":
            self.show_statistiques()
        elif page == "quetes":
            self.show_quetes()
        elif page == "marche":
            self.show_marche()
        elif page == "combat":
            self.show_combat()
    
    def show_boutique(self):
        title = ctk.CTkLabel(self.content_frame, text="🏪 Boutique Exclusive", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Afficher les articles
        for i, article in enumerate(self.articles):
            self.create_article_widget(scroll_frame, article, i)
    
    def create_article_widget(self, parent, article, index):
        # Couleurs selon la rareté
        rarity_colors = {
            "Commun": ("#95A5A6", "#7F8C8D"),
            "Rare": ("#3498DB", "#2980B9"),
            "Épique": ("#9B59B6", "#8E44AD"),
            "Légendaire": ("#F39C12", "#E67E22"),
            "Mythique": ("#E74C3C", "#C0392B"),
            "Impossible": ("#303030", "#141414")
        }
        
        color = rarity_colors.get(article.get("rareté", "Commun"), rarity_colors["Commun"])
        
        article_frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        article_frame.pack(fill="x", pady=5, padx=10)
        
        # Contenu de l'article
        content_frame = ctk.CTkFrame(article_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Nom et rareté
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x")
        
        name_label = ctk.CTkLabel(name_frame, text=article["nom"], 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        name_label.pack(side="left")
        
        rarity_label = ctk.CTkLabel(name_frame, text=f"[{article.get('rareté', 'Commun')}]", 
                                   font=ctk.CTkFont(size=12))
        rarity_label.pack(side="right")
        
        # Description
        desc_label = ctk.CTkLabel(content_frame, text=article["description"], 
                                 font=ctk.CTkFont(size=12), 
                                 text_color="gray90")
        desc_label.pack(anchor="w", pady=(5, 10))
        
        # Prix et bouton
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")
        
        price_label = ctk.CTkLabel(bottom_frame, text=f"💰 {article['prix']} écus", 
                                  font=ctk.CTkFont(size=14, weight="bold"))
        price_label.pack(side="left")
        
        if article["achats"] > 0:
            bought_label = ctk.CTkLabel(bottom_frame, text=f"Acheté {article['achats']} fois", 
                                       font=ctk.CTkFont(size=10))
            bought_label.pack(side="left", padx=(20, 0))
        
        buy_btn = ctk.CTkButton(bottom_frame, text="Acheter", width=100,
                               command=lambda idx=index: self.acheter_article(idx))
        buy_btn.pack(side="right")
    
    def acheter_article(self, index):
        article = self.articles[index]
        if self.ecus >= article["prix"]:
            self.ecus -= article["prix"]
            self.inventaire.append(dict(article))
            article["achats"] += 1
            
            self.historique_achats.append({
                "article": article["nom"],
                "prix": article["prix"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.experience += 10
            self.check_level_up()
            self.check_quetes()
            
            self.notifications.show_notification(f"✅ {article['nom']} acheté avec succès!", "success")
            self.update_display()
            self.save_data()
        else:
            self.notifications.show_notification("❌ Écus insuffisants!", "error")
    
    def show_banque(self):
        title = ctk.CTkLabel(self.content_frame, text="🏦 Banque Centrale", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Informations bancaires
        info_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        balance_label = ctk.CTkLabel(info_frame, text=f"💰 Solde en banque: {self.ecus_banque} écus", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        balance_label.pack(pady=20)
        
        wallet_label = ctk.CTkLabel(info_frame, text=f"👛 Écus en main: {self.ecus} écus", 
                                   font=ctk.CTkFont(size=16))
        wallet_label.pack(pady=10)
        
        # Opérations bancaires
        operations_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        operations_frame.pack(fill="x", padx=20, pady=10)
        
        # Déposer
        deposit_frame = ctk.CTkFrame(operations_frame, fg_color="transparent")
        deposit_frame.pack(fill="x", padx=20, pady=15)
        
        deposit_label = ctk.CTkLabel(deposit_frame, text="Déposer des écus:")
        deposit_label.pack(anchor="w")
        
        self.deposit_entry = ctk.CTkEntry(deposit_frame, placeholder_text="Montant à déposer")
        self.deposit_entry.pack(fill="x", pady=5)
        
        deposit_btn = ctk.CTkButton(deposit_frame, text="💾 Déposer", 
                                   command=self.deposer_argent)
        deposit_btn.pack(pady=5)
        
        # Retirer
        withdraw_frame = ctk.CTkFrame(operations_frame, fg_color="transparent")
        withdraw_frame.pack(fill="x", padx=20, pady=15)
        
        withdraw_label = ctk.CTkLabel(withdraw_frame, text="Retirer des écus:")
        withdraw_label.pack(anchor="w")
        
        self.withdraw_entry = ctk.CTkEntry(withdraw_frame, placeholder_text="Montant à retirer")
        self.withdraw_entry.pack(fill="x", pady=5)
        
        withdraw_btn = ctk.CTkButton(withdraw_frame, text="💸 Retirer", 
                                    command=self.retirer_argent)
        withdraw_btn.pack(pady=5)
        
        # Prêt (nouveau)
        loan_frame = ctk.CTkFrame(operations_frame, fg_color="transparent")
        loan_frame.pack(fill="x", padx=20, pady=15)
        
        loan_label = ctk.CTkLabel(loan_frame, text="Demander un prêt (5% d'intérêt):")
        loan_label.pack(anchor="w")
        
        loan_btn = ctk.CTkButton(loan_frame, text="💳 Prêt de 500 écus", 
                                command=self.demander_pret)
        loan_btn.pack(pady=5)
    
    def deposer_argent(self):
        try:
            montant = int(self.deposit_entry.get())
            if montant > 0 and montant <= self.ecus:
                self.ecus -= montant
                self.ecus_banque += montant
                self.experience += 5
                self.check_quetes()
                self.notifications.show_notification(f"✅ {montant} écus déposés!", "success")
                self.update_display()
                self.save_data()
                self.deposit_entry.delete(0, "end")
            else:
                self.notifications.show_notification("❌ Montant invalide!", "error")
        except ValueError:
            self.notifications.show_notification("❌ Veuillez entrer un nombre valide!", "error")
    
    def retirer_argent(self):
        try:
            montant = int(self.withdraw_entry.get())
            if montant > 0 and montant <= self.ecus_banque:
                self.ecus_banque -= montant
                self.ecus += montant
                self.notifications.show_notification(f"✅ {montant} écus retirés!", "success")
                self.update_display()
                self.save_data()
                self.withdraw_entry.delete(0, "end")
            else:
                self.notifications.show_notification("❌ Fonds insuffisants!", "error")
        except ValueError:
            self.notifications.show_notification("❌ Veuillez entrer un nombre valide!", "error")
    
    def demander_pret(self):
        if self.ecus_banque >= 100:  # Garantie minimale
            self.ecus += 500
            self.ecus_banque -= 100  # Frais
            self.notifications.show_notification("✅ Prêt accordé! 100 écus de frais prélevés.", "success")
            self.update_display()
            self.save_data()
        else:
            self.notifications.show_notification("❌ Garantie insuffisante (100 écus minimum en banque)!", "error")
    
    def show_inventaire(self):
        title = ctk.CTkLabel(self.content_frame, text="🎒 Mon Inventaire", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        if not self.inventaire:
            empty_label = ctk.CTkLabel(self.content_frame, text="Votre inventaire est vide", 
                                      font=ctk.CTkFont(size=16))
            empty_label.pack(pady=50)
            return
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, item in enumerate(self.inventaire):
            item_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
            item_frame.pack(fill="x", pady=5, padx=10)
            
            content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=15)
            
            name_label = ctk.CTkLabel(content_frame, text=item["nom"], 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            name_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(content_frame, text=item["description"], 
                                     font=ctk.CTkFont(size=12))
            desc_label.pack(anchor="w", pady=5)
            
            rarity_label = ctk.CTkLabel(content_frame, text=f"Rareté: {item.get('rareté', 'Commun')}", 
                                       font=ctk.CTkFont(size=10))
            rarity_label.pack(anchor="w")
    
    def show_vendre(self):
        title = ctk.CTkLabel(self.content_frame, text="💼 Vendre des Articles", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        if not self.inventaire:
            empty_label = ctk.CTkLabel(self.content_frame, text="Aucun article à vendre", 
                                      font=ctk.CTkFont(size=16))
            empty_label.pack(pady=50)
            return
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, item in enumerate(self.inventaire):
            item_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
            item_frame.pack(fill="x", pady=5, padx=10)
            
            content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=15)
            
            # Informations de l'article
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)
            
            name_label = ctk.CTkLabel(info_frame, text=item["nom"], 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            name_label.pack(anchor="w")
            
            prix_vente = int(item["prix"] * 0.7)  # 70% du prix original
            price_label = ctk.CTkLabel(info_frame, text=f"Prix de vente: {prix_vente} écus", 
                                      font=ctk.CTkFont(size=14))
            price_label.pack(anchor="w", pady=5)
            
            # Bouton vendre
            sell_btn = ctk.CTkButton(content_frame, text="Vendre", width=100,
                                    command=lambda idx=i: self.vendre_article(idx))
            sell_btn.pack(side="right", padx=10)
    
    def vendre_article(self, index):
        if 0 <= index < len(self.inventaire):
            item = self.inventaire[index]
            prix_vente = int(item["prix"] * 0.7)
            
            self.ecus += prix_vente
            self.inventaire.pop(index)
            
            self.historique_ventes.append({
                "article": item["nom"],
                "prix": prix_vente,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.experience += 5
            self.check_level_up()
            self.check_quetes()
            
            self.notifications.show_notification(f"✅ {item['nom']} vendu pour {prix_vente} écus!", "success")
            self.update_display()
            self.save_data()
            
            # Recharger la page vendre
            self.show_vendre()
    
    def show_statistiques(self):
        title = ctk.CTkLabel(self.content_frame, text="📊 Statistiques", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        stats_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Statistiques générales
        general_frame = ctk.CTkFrame(stats_frame, corner_radius=10)
        general_frame.pack(fill="x", padx=20, pady=20)
        
        general_title = ctk.CTkLabel(general_frame, text="📈 Statistiques Générales", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        general_title.pack(pady=10)
        
        stats_text = f"""
⭐ Niveau: {self.niveau}
🎯 Expérience: {self.experience} XP
💰 Écus totaux: {self.ecus + self.ecus_banque}
🛍️ Articles dans l'inventaire: {len(self.inventaire)}
🛒 Achats effectués: {len(self.historique_achats)}
💼 Ventes effectuées: {len(self.historique_ventes)}
        """
        
        stats_label = ctk.CTkLabel(general_frame, text=stats_text, 
                                  font=ctk.CTkFont(size=14))
        stats_label.pack(pady=10)
        
        # Historique des achats
        if self.historique_achats:
            history_frame = ctk.CTkFrame(stats_frame, corner_radius=10)
            history_frame.pack(fill="x", padx=20, pady=10)
            
            history_title = ctk.CTkLabel(history_frame, text="🛒 Derniers Achats", 
                                        font=ctk.CTkFont(size=18, weight="bold"))
            history_title.pack(pady=10)
            
            for achat in self.historique_achats[-5:]:  # 5 derniers achats
                achat_text = f"• {achat['article']} - {achat['prix']} écus ({achat['date']})"
                achat_label = ctk.CTkLabel(history_frame, text=achat_text, 
                                          font=ctk.CTkFont(size=12))
                achat_label.pack(anchor="w", padx=20, pady=2)
    
    def show_quetes(self):
        title = ctk.CTkLabel(self.content_frame, text="🎯 Quêtes", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for quete in self.quetes:
            color = ("#2ECC71", "#27AE60") if quete["complete"] else ("#3498DB", "#2980B9")
            
            quete_frame = ctk.CTkFrame(scroll_frame, fg_color=color, corner_radius=10)
            quete_frame.pack(fill="x", pady=5, padx=10)
            
            content_frame = ctk.CTkFrame(quete_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=15)
            
            name_label = ctk.CTkLabel(content_frame, text=quete["nom"], 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            name_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(content_frame, text=quete["description"], 
                                     font=ctk.CTkFont(size=12))
            desc_label.pack(anchor="w", pady=5)
            
            reward_label = ctk.CTkLabel(content_frame, text=f"Récompense: {quete['recompense']} écus", 
                                       font=ctk.CTkFont(size=12, weight="bold"))
            reward_label.pack(anchor="w", pady=2)
            
            status_text = "✅ Terminée" if quete["complete"] else "🔄 En cours"
            status_label = ctk.CTkLabel(content_frame, text=status_text, 
                                       font=ctk.CTkFont(size=12))
            status_label.pack(anchor="w", pady=2)
    
    def show_marche(self):
        title = ctk.CTkLabel(self.content_frame, text="📈 Marché des Changes", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        market_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        market_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Générateur de prix aléatoires
        exchange_rates = {
            "Or": round(random.uniform(0.8, 1.2), 2),
            "Diamant": round(random.uniform(2.0, 3.5), 2),
            "Cristal": round(random.uniform(1.5, 2.0), 2),
            "Argent": round(random.uniform(0.5, 0.8), 2)
        }
        
        market_title = ctk.CTkLabel(market_frame, text="💱 Taux de Change", 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        market_title.pack(pady=20)
        
        for currency, rate in exchange_rates.items():
            rate_frame = ctk.CTkFrame(market_frame, corner_radius=10)
            rate_frame.pack(fill="x", padx=20, pady=5)
            
            rate_content = ctk.CTkFrame(rate_frame, fg_color="transparent")
            rate_content.pack(fill="x", padx=15, pady=10)
            
            currency_label = ctk.CTkLabel(rate_content, text=f"{currency}: {rate} écus", 
                                         font=ctk.CTkFont(size=14, weight="bold"))
            currency_label.pack(side="left")
            
            # Simuler des variations
            variation = random.choice(["+", "-"])
            var_percent = round(random.uniform(0.1, 5.0), 1)
            var_color = "green" if variation == "+" else "red"
            
            var_label = ctk.CTkLabel(rate_content, text=f"{variation}{var_percent}%", 
                                    font=ctk.CTkFont(size=12), text_color=var_color)
            var_label.pack(side="right")
        
        # Bouton pour actualiser les taux
        refresh_btn = ctk.CTkButton(market_frame, text="🔄 Actualiser les taux", 
                                   command=lambda: self.show_marche())
        refresh_btn.pack(pady=20)
    
    def show_combat(self):
        title = ctk.CTkLabel(self.content_frame, text="⚔️ Arène de Combat", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        combat_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        combat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Statistiques du joueur
        player_stats_frame = ctk.CTkFrame(combat_frame, corner_radius=10)
        player_stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_title = ctk.CTkLabel(player_stats_frame, text="👤 Vos Statistiques", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        stats_title.pack(pady=10)
        
        # Calculer les stats basées sur l'inventaire
        attack = 10 + len([item for item in self.inventaire if "Épée" in item["nom"] or "Gants" in item["nom"]]) * 5
        defense = 10 + len([item for item in self.inventaire if "Armure" in item["nom"] or "Bouclier" in item["nom"]]) * 3
        magic = 5 + len([item for item in self.inventaire if "Grimoire" in item["nom"] or "Bague" in item["nom"]]) * 4
        
        stats_text = f"""
⚔️ Attaque: {attack}
🛡️ Défense: {defense}
🔮 Magie: {magic}
❤️ Points de Vie: {100 + self.niveau * 10}
        """
        
        stats_label = ctk.CTkLabel(player_stats_frame, text=stats_text, 
                                  font=ctk.CTkFont(size=14))
        stats_label.pack(pady=10)
        
        # Ennemis disponibles
        enemies_frame = ctk.CTkFrame(combat_frame, corner_radius=10)
        enemies_frame.pack(fill="x", padx=20, pady=10)
        
        enemies_title = ctk.CTkLabel(enemies_frame, text="👹 Choisir un Adversaire", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        enemies_title.pack(pady=10)
        
        enemies = [
            {"nom": "Gobelin", "niveau": 1, "recompense": 25},
            {"nom": "Orc", "niveau": 3, "recompense": 75},  
            {"nom": "Dragon", "niveau": 5, "recompense": 200},
            {"nom": "Liche", "niveau": 8, "recompense": 500}
        ]
        
        for enemy in enemies:
            if self.niveau >= enemy["niveau"]:
                enemy_frame = ctk.CTkFrame(enemies_frame, corner_radius=10)
                enemy_frame.pack(fill="x", padx=20, pady=5)
                
                enemy_content = ctk.CTkFrame(enemy_frame, fg_color="transparent")
                enemy_content.pack(fill="x", padx=15, pady=10)
                
                enemy_info = ctk.CTkLabel(enemy_content, 
                                         text=f"{enemy['nom']} (Niveau {enemy['niveau']}) - Récompense: {enemy['recompense']} écus", 
                                         font=ctk.CTkFont(size=14))
                enemy_info.pack(side="left")
                
                fight_btn = ctk.CTkButton(enemy_content, text="⚔️ Combattre", width=100,
                                         command=lambda e=enemy: self.combat(e))
                fight_btn.pack(side="right")
    
    def combat(self, enemy):
        # Simulation de combat simple
        player_power = self.niveau * 10 + len(self.inventaire) * 5
        enemy_power = enemy["niveau"] * 8
        
        # Ajouter de l'aléatoire
        player_roll = random.randint(1, 20) + player_power
        enemy_roll = random.randint(1, 20) + enemy_power
        
        if player_roll > enemy_roll:
            self.ecus += enemy["recompense"]
            self.experience += enemy["niveau"] * 15
            self.check_level_up()
            self.notifications.show_notification(f"🏆 Victoire contre {enemy['nom']}! +{enemy['recompense']} écus!", "success")
        else:
            perte = min(self.ecus, 20)
            self.ecus -= perte
            self.notifications.show_notification(f"💀 Défaite contre {enemy['nom']}... -{perte} écus", "error")
        
        self.update_display()
        self.save_data()
    
    def show_add_article_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Ajouter un Article")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        title = ctk.CTkLabel(dialog, text="➕ Nouvel Article", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Formulaire
        form_frame = ctk.CTkFrame(dialog, corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nom
        name_label = ctk.CTkLabel(form_frame, text="Nom de l'article:")
        name_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Épée Magique")
        name_entry.pack(fill="x", padx=20, pady=5)
        
        # Prix
        price_label = ctk.CTkLabel(form_frame, text="Prix:")
        price_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        price_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 100")
        price_entry.pack(fill="x", padx=20, pady=5)
        
        # Description
        desc_label = ctk.CTkLabel(form_frame, text="Description:")
        desc_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        desc_entry = ctk.CTkTextbox(form_frame, height=60)
        desc_entry.pack(fill="x", padx=20, pady=5)
        
        # Rareté
        rarity_label = ctk.CTkLabel(form_frame, text="Rareté:")
        rarity_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        rarity_var = ctk.StringVar(value="Commun")
        rarity_menu = ctk.CTkOptionMenu(form_frame, values=["Commun", "Rare", "Épique", "Légendaire", "Mythique"],
                                       variable=rarity_var)
        rarity_menu.pack(fill="x", padx=20, pady=5)
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        def ajouter_article():
            try:
                nom = name_entry.get().strip()
                prix = int(price_entry.get())
                description = desc_entry.get("1.0", "end-1c").strip()
                rarete = rarity_var.get()
                
                if nom and prix > 0 and description:
                    nouvel_article = {
                        "nom": nom,
                        "prix": prix,
                        "achats": 0,
                        "description": description,
                        "rareté": rarete
                    }
                    
                    self.articles.append(nouvel_article)
                    self.save_data()
                    self.notifications.show_notification(f"✅ Article '{nom}' ajouté avec succès!", "success")
                    dialog.destroy()
                    
                    # Recharger la boutique si on y est
                    if self.current_page == "boutique":
                        self.show_boutique()
                else:
                    self.notifications.show_notification("❌ Veuillez remplir tous les champs!", "error")
                    
            except ValueError:
                self.notifications.show_notification("❌ Le prix doit être un nombre!", "error")
        
        add_btn = ctk.CTkButton(buttons_frame, text="✅ Ajouter", 
                               command=ajouter_article)
        add_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="❌ Annuler", 
                                  command=dialog.destroy)
        cancel_btn.pack(side="right", padx=5)
    
    def check_level_up(self):
        new_level = (self.experience // 100) + 1
        if new_level > self.niveau:
            self.niveau = new_level
            bonus_ecus = self.niveau * 50
            self.ecus += bonus_ecus
            self.notifications.show_notification(f"🎉 Niveau {self.niveau} atteint! +{bonus_ecus} écus bonus!", "success")
    
    def check_quetes(self):
        for quete in self.quetes:
            if not quete["complete"]:
                completed = False
                
                if quete["type"] == "achat" and len(self.historique_achats) >= quete["objectif"]:
                    completed = True
                elif quete["type"] == "vente" and len(self.historique_ventes) >= quete["objectif"]:
                    completed = True
                elif quete["type"] == "banque" and self.ecus_banque >= quete["objectif"]:
                    completed = True
                elif quete["type"] == "niveau" and self.niveau >= quete["objectif"]:
                    completed = True
                
                if completed:
                    quete["complete"] = True
                    self.ecus += quete["recompense"]
                    self.notifications.show_notification(f"🎯 Quête '{quete['nom']}' terminée! +{quete['recompense']} écus!", "success")
    
    def update_display(self):
        self.ecus_label.configure(text=f"💰 {self.ecus}")
        self.level_label.configure(text=f"⭐ Niveau {self.niveau} (XP: {self.experience})")
    
    def save_data(self):
        data = {
            "ecus": self.ecus,
            "ecus_banque": self.ecus_banque,
            "experience": self.experience,
            "niveau": self.niveau,
            "inventaire": self.inventaire,
            "articles": self.articles,
            "historique_achats": self.historique_achats,
            "historique_ventes": self.historique_ventes,
            "quetes": self.quetes
        }
        
        try:
            with open("boutique_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.notifications.show_notification(f"❌ Erreur de sauvegarde: {str(e)}", "error")
    
    def load_data(self):
        try:
            if os.path.exists("boutique_data.json"):
                with open("boutique_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.ecus = data.get("ecus", 1000)
                self.ecus_banque = data.get("ecus_banque", 0)
                self.experience = data.get("experience", 0)
                self.niveau = data.get("niveau", 1)
                self.inventaire = data.get("inventaire", [])
                self.historique_achats = data.get("historique_achats", [])
                self.historique_ventes = data.get("historique_ventes", [])
                self.quetes = data.get("quetes", self.quetes)
                
                # Mettre à jour les articles existants
                saved_articles = data.get("articles", [])
                if saved_articles:
                    # Fusionner avec les nouveaux articles tout en gardant les stats d'achat
                    for saved_article in saved_articles:
                        for article in self.articles:
                            if article["nom"] == saved_article["nom"]:
                                article["achats"] = saved_article.get("achats", 0)
                                break
                        else:
                            # Ajouter les articles personnalisés sauvegardés
                            self.articles.append(saved_article)
                
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BoutiqueShop()
    app.run()

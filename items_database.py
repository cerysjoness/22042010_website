from app4 import app, db, Shirt

shirts = [
    { "name": "Liverpool Home Shirt 1982/84", "price": "£35", "image": "liverpool_home_82-84.jpg", "description": "0.55 CO₂/kg", "detailedDescription": "The Liverpool Home Shirt from the 1982 to 1984 seasons is a classic and iconic piece of football memorabilia, cherished by fans for its distinctive design and historical significance. This shirt features the traditional Liverpool red color with simple yet distinctive white accents, most notably the thin white stripes down the sleeves and around the v-neck collar. The shirt also sports the classic Liverpool crest on the left chest, along with the emblem of their sponsor at the time. This period was a successful era for Liverpool FC, under the management of Bob Paisley and later Joe Fagan. The team won several major trophies during these years, including the League Championship and the European Cup. The 1982/84 home shirt, therefore, represents not just a stylish piece of sportswear but also a symbol of Liverpool's dominance in football during the early 1980s. It's a must-have for collectors and fans who appreciate the club's rich history." },
    { "name": "Chelsea Home Shirt 1982/83", "price": "£45", "image": "chelsea_82-83.jpg", "description": "0.75 CO₂/kg", "detailedDescription": "The Chelsea Home Shirt from the 1982/83 season is a classic, featuring the club's traditional royal blue with white trim around the V-neck collar and sleeves. This clean, sponsor-free design reflects the early 1980s football kit style. Despite Chelsea's struggles in the Second Division that season, this shirt remains a cherished piece of the club's rich history, appreciated by fans and collectors alike."},   
    { "name": "Manchester United Home Shirt 1984", "price": "£45", "image": "man_united_84.jpg", "description": "0.81 CO₂/kg", "detailedDescription": "The Manchester United Home Shirt from 1984 is a classic piece of football memorabilia, featuring the team's iconic red with white accents on the collar and cuffs. This shirt is especially noted for its sharp and traditional look, emblematic of the era's football kit styles. The Manchester United crest is prominently displayed, along with the sponsor logo, which was a new addition at the time, adding to its historic value. This shirt represents a significant period in Manchester United's history, capturing the essence of 1980s football fashion."},    
    { "name": "Tottenham Hotspurs Home Shirt 1994", "price": "£45", "image": "tottenham_94.jpg", "description": "0.49 CO₂/kg", "detailedDescription": "The Tottenham Hotspur Home Shirt from 1994 is distinguished by its classic white design with navy blue trim, reflecting Tottenham's traditional colors. This shirt features a distinctive collar and the club’s crest prominently displayed on the chest, alongside the sponsor's logo. The 1994 shirt is remembered for its stylish design during a period of significant changes within the club and is highly regarded among fans for its aesthetic appeal and connection to a transitional era for Tottenham."},
]

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 

        existing_shirts = Shirt.query.filter(Shirt.name.in_([shirt['name'] for shirt in shirts])).all()    
        for existing_shirt in existing_shirts:
            db.session.delete(existing_shirt)

        db.session.commit()

        for shirt_data in shirts:
            new_shirt = Shirt(name=shirt_data["name"], price=shirt_data["price"], image=shirt_data["image"], description=shirt_data["description"], detailedDescription=shirt_data["detailedDescription"])
            db.session.add(new_shirt)        

        db.session.commit()

        
const menuWeeks = [
  {
    title: "Semaine 1 — du lundi 27 avril au vendredi 1 mai",
    days: [
      { day: "Lundi", starter: "Salade de crudités", main: "Poulet rôti, légumes vapeur", dessert: "Compote de pommes" },
      { day: "Mardi", starter: "Soupe de légumes", main: "Poisson, riz parfumé", dessert: "Yaourt nature" },
      { day: "Mercredi", starter: "Concombres vinaigrette", main: "Pâtes aux légumes grillés", dessert: "Banane" },
      { day: "Jeudi", starter: "Betteraves", main: "Steak haché, purée", dessert: "Flan vanille" },
      { day: "Vendredi", starter: "Salade verte", main: "Gratin de pommes de terre", dessert: "Salade de fruits" }
    ]
  },
  {
    title: "Semaine 2 — du lundi 4 mai au vendredi 8 mai",
    days: [
      { day: "Lundi", starter: "Tomates mozzarella", main: "Escalope de dinde, haricots verts", dessert: "Poire" },
      { day: "Mardi", starter: "Velouté de courgettes", main: "Cabillaud, semoule", dessert: "Crème dessert" },
      { day: "Mercredi", starter: "Carottes râpées", main: "Lasagnes végétariennes", dessert: "Pomme" },
      { day: "Jeudi", starter: "Taboulé", main: "Boulettes de bœuf, riz", dessert: "Yaourt aux fruits" },
      { day: "Vendredi", starter: "Salade de maïs", main: "Omelette, pommes sautées", dessert: "Orange" }
    ]
  },
  {
    title: "Semaine 3 — du lundi 11 mai au vendredi 15 mai",
    days: [
      { day: "Lundi", starter: "Salade de chou", main: "Poulet curry doux, riz", dessert: "Compote poire" },
      { day: "Mardi", starter: "Soupe de tomates", main: "Poisson pané, purée", dessert: "Crème caramel" },
      { day: "Mercredi", starter: "Salade verte", main: "Pâtes bolognaises", dessert: "Clémentine" },
      { day: "Jeudi", starter: "Macédoine", main: "Sauté de veau, légumes", dessert: "Yaourt" },
      { day: "Vendredi", starter: "Crudités", main: "Quiche légumes, salade", dessert: "Compote" }
    ]
  },
  {
    title: "Semaine 4 — du lundi 18 mai au vendredi 22 mai",
    days: [
      { day: "Lundi", starter: "Concombres", main: "Rôti de dinde, gratin", dessert: "Pêche" },
      { day: "Mardi", starter: "Potage maison", main: "Saumon, pâtes", dessert: "Flan chocolat" },
      { day: "Mercredi", starter: "Betteraves", main: "Couscous végétarien", dessert: "Pomme" },
      { day: "Jeudi", starter: "Salade de lentilles", main: "Steak, légumes", dessert: "Yaourt vanille" },
      { day: "Vendredi", starter: "Salade composée", main: "Pizza légumes", dessert: "Salade de fruits" }
    ]
  },
  {
    title: "Semaine 5 — du lundi 25 mai au vendredi 29 mai",
    days: [
      { day: "Lundi", starter: "Tomates", main: "Poulet sauce légère, riz", dessert: "Compote" },
      { day: "Mardi", starter: "Velouté", main: "Colin, pommes vapeur", dessert: "Banane" },
      { day: "Mercredi", starter: "Carottes râpées", main: "Pâtes au saumon", dessert: "Yaourt fruits rouges" },
      { day: "Jeudi", starter: "Salade verte", main: "Bœuf mijoté, purée", dessert: "Orange" },
      { day: "Vendredi", starter: "Crudités", main: "Tarte salée, salade", dessert: "Crème dessert" }
    ]
  }
];

let currentWeekIndex = 0;
let currentDayIndex = 0;

function renderMenuDay() {
  const weekTitle = document.getElementById("menu-week-title");
  const dayTitle = document.getElementById("menu-day-title");
  const menuDay = document.getElementById("single-menu-day");

  if (!weekTitle || !dayTitle || !menuDay) return;

  const week = menuWeeks[currentWeekIndex];
  const day = week.days[currentDayIndex];

  weekTitle.textContent = week.title;
  dayTitle.textContent = day.day;

  menuDay.innerHTML = `
    <div class="menu-line"><span class="menu-label">Entrée :</span> ${day.starter}</div>
    <div class="menu-line"><span class="menu-label">Plat :</span> ${day.main}</div>
    <div class="menu-line"><span class="menu-label">Dessert :</span> ${day.dessert}</div>
  `;
}

function nextDay() {
  currentDayIndex++;

  if (currentDayIndex >= menuWeeks[currentWeekIndex].days.length) {
    currentDayIndex = 0;
    currentWeekIndex = (currentWeekIndex + 1) % menuWeeks.length;
  }

  renderMenuDay();
}

function previousDay() {
  currentDayIndex--;

  if (currentDayIndex < 0) {
    currentWeekIndex = (currentWeekIndex - 1 + menuWeeks.length) % menuWeeks.length;
    currentDayIndex = menuWeeks[currentWeekIndex].days.length - 1;
  }

  renderMenuDay();
}

document.addEventListener("DOMContentLoaded", renderMenuDay);

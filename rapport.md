# La Caverne d'AliBaba  <!-- omit from toc -->
**Alieldeen Ibrahim**  
Groupe 402

Travail de Maturité  
Maître accompgnant : **M. Mathieu Schiess**

*COLLÈGE SISMONDI*

___

- [Le *Tech Stack*](#le-tech-stack)
  - [*Backend*](#backend)
  - [*Frontend*](#frontend)
  - [*Database* (base de données)](#database-base-de-données)
  - [*Cloud storage*](#cloud-storage)

---

<br>

À travers son parcours academique, on fait tous.tes face aux évaluations, c'est malheuresement inevitable. Il arrive parfois que, au moment de la révision pour une des ces fameuses évaluations, les fiches de théorie données pour son/sa prof n'aident pas vraiment, ou on n'a plus d'exercices pour s'entrainer parce que celui/celle n'en fait tout simplement très peu. Il est bien evidement possible de chercher sur l'internet, mais c'est très difficile de trouver des exercices avec la même difficulté que celle qu'on fait en cours, ou de trouver le sujet expliqué de la même manière que son/sa adorable prof. Il est aussi possible de demander à ses amis, mais quel.le ami.e ? Celle qui vient presque jamais en cours ? Celui qui ne note quasiment rien ? C'est pourquoi j'ai decidé de faire un site web qui permet de partager tous ses fichiers afin de faciliter le recherche ceux-ci dans les moments les plus (ou les moins) urgents.

## Le *Tech Stack*

La definition du *Tech Stack* sur [GeeksForGeeks](https://www.geeksforgeeks.org/blogs/what-are-tech-stacks-choosing-the-right-one/) : 

> A tech stack (technology stack) is the collection of tools, frameworks, programming languages, and platforms used to build and run a web or mobile application. It represents the layered foundation of modern software where each component works together to enable functionality, performance, and scalability.  

Le *Tech stack* se divise en 4 parties principales:

- ***Frontend*** : Les technologies definissant ce que le client voit et interagit avec. Elle est aussi appelée *Client-side*.
- ***Backend*** : Les technologies responsables pour la logique de l'application, le traitement et la gestion des données. C'est ce qui se passe "en coulisse". Elle est aussi appelée *Server-side*.
- ***Database*** **(base de données)** : C'est ici qu'on stocke et gère les données.
- **Infrastructure** : Il s'agit de la mise en production (*deployment*), le *cloud*, etc.

Il existe une quantité enorme de *stacks* dont les plus populaires utilisent JavaScript comme langage principale (e.g. MERN, MEAN, MEVN, etc.). Il y aussi d'autres basés sur d'autres langages comme *Ruby on rails* pour Ruby, *Spring* pour Java, *.NET* pour C#, *Django* et *Flask* pour Python, et plein d'autres.  
Je vous prèsente donc le stack pour lequel j'ai opté.

### *Backend*

Le langage que je connais le mieux est Python, donc mon choix de *framework* était entre *Django* et *Flask*. Comme tout, chacun a ses propres avantages et désavantages.  

Commençons par Django. Django, publiée en 2005, est une *framework* qu'on dit est *batteries included*, c'est-à-dire qu'elle te donne tout ce dont on a besion *out of the box*. Elle est magnifique pour des grands applications, mais *overkill* pour des petits projets ou des microservices. Elle est très bien [documentée](https://docs.djangoproject.com/) avec une grande communauté. Il existe une quantité énorme de tutos en ligne pour presque tout les choses qu'on aimerait faire. Il est important de savoir que Django est utilisé par pleins d'applications notamment Instagram, Spotify, YouTube, Pinterest, Mozilla et autres.

Inversement, Flask est très minimale, on ne te donne rien au début. Ceci peut être bon et mauvais selon les cas. Bon car elle permet une grande flexibilité, ce qui est très bien pour commencer très rapidement un projet assez petit, mauvais quand le projet est assez grand. Ainsi, elle necessite soit l'installation de beaucoup de modules pour faire la même chose que Django soit la création soi-même de ses modules. Voici une liste non exhaustive des modules à installer si je travaillais avec Flask :  

Fonctionnalité | Module
---------------|----------
 ORM | SQLAlchemy et Flask-SQLAlchemy 
 Authentification | Flask-login 
 Validation et Création des forms | WTForms et Flask-WTF
 Interface d'admin | Flask-admin
 ...

De plus, ces modules ne sont pas toujours bien documentés, cependant, Flask elle-même est aussi bien documentée avec une communauté un peu moins large que celle de Django. Flask est utilisé plutôt par des entreprises pour faire des microservices, ce qui est le cas pour Netflix, Pinterest, Airbnb.

J'ai donc choisi de faire ce projet avec Django pour les raisons listées ci-dessus.


### *Frontend*

 J'ai choisi de ne pas utiliser une *frontend framework*, car je trouve que l'application n'a pas besion de la complexité qu'amène une comme *React* or *Vue*. À savoir que pour utiliser une *frontend*, on devrais écrire un API qui sert les informations à cette dernière (CSR, dit *Client-side rendering*) au lieu d'utiliser les *templates* de Django pour générer l'HTML côté serveur (SSR, dit *Server-side rendering*), ce qui, à mon avis, rend les choses plus compliquées. Cependant, il faut quand même du dynamisme dans le sit, je vais donc utliser Vanilla JS (ou HTMX). (HTMX est un entre-deux. Elle m'évite d'écrire beaucoup de *boilerplate*. Si j'écrivais tout en Vanilla JS, je serais essentiellment en train d'écrire mon propre *Framework*). J'ai choisi d'utiliser *Bootstrap* au lieu d'écrire moi-même le CSS car elle permet de faire le *design* qu'on le veut en très peu de temps.


### *Database* (base de données)

PostgreSQL

### *Cloud storage*

AWS S3 buckets, Google Cloud



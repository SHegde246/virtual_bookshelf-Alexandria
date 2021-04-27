from django.db import models
from django.conf import settings
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

OPTIONS=((1, 'Absurdist fiction'), (2, 'Adventure'), (3, 'Adventure novel'), (4, 'Albino bias'), (5, 'Alien invasion'), (6, 'Alternate history'), (7, 'American Gothic Fiction'), (8, 'Anthology'), (9, 'Anthropology'), (10, 'Anti-nuclear'), (11, 'Anti-war'), (12, 'Apocalyptic and post-apocalyptic fiction'), (13, 'Autobiography'), (14, 'Bangsian fantasy'), (15, 'Bildungsroman'), (16, 'Biographical novel'), (17, 'Biography'), (18, 'Biopunk'), (19, 'Bit Lit'), (20, 'Black comedy'), (21, 'Boys school stories'), (22, 'Business'), (23, 'Cabal'), (24, 'Campus novel'), (25, 'Catastrophic literature'), (26, 'Chick lit'), (27, "Children's literature"), (28, 'Collage'), (29, 'Comedy'), (30, 'Comedy of manners'), (31, 'Comics'), (32, 'Coming of age'), (33, 'Computer Science'), (34, 'Conspiracy'), (35, 'Contemporary fantasy'), (36, 'Cookbook'), (37, 'Cozy'), (38, 'Creative nonfiction'), (39, 'Crime Fiction'), (40, 'Cyberpunk'), (41, 'Dark fantasy'), (42, 'Detective fiction'), (43, 'Drama'), (44, 'Dying Earth subgenre'), (45, 'Dystopia'), (46, 'Economics'), (47, 'Edisonade'), (48, 'Education'), (49, 'Encyclopedia'), (50, 'English public-school stories'), (51, 'Epic Science Fiction and Fantasy'), (52, 'Epistolary novel'), (53, 'Ergodic literature'), (54, 'Erotica'), (55, 'Essay'), (56, 'Existentialism'), (57, 'Experimental literature'), (58, 'Fable'), (59, 'Fairy tale'), (60, 'Fairytale fantasy'), (61, 'Fantastique'), (62, 'Fantasy'), (63, 'Fantasy of manners'), (64, 'Farce'), (65, 'Feminist science fiction'), (66, 'Fiction'), (67, 'Fictional crossover'), (68, 'Field guide'), (69, 'First-person narrative'), (70, 'Foreign legion'), (71, 'Future history'), (72, 'Gamebook'), (73, 'Ghost story'), (74, 'Gothic fiction'), (75, 'Graphic novel'), (76, 'Hard science fiction'), (77, 'Hardboiled'), (78, 'Heroic fantasy'), (79, 'High fantasy'), (80, 'Historical fantasy'), (81, 'Historical fiction'), (82, 'Historical novel'), (83, 'Historical whodunnit'), (84, 'History'), (85, 'Horror'), (86, 'Human extinction'), (87, 'Humour'), (88, 'Industrial novel'), (89, 'Inspirational'), (90, 'Invasion literature'), (91, 'Juvenile fantasy'), (92, 'Künstlerroman'), (93, 'LGBT literature'), (94, 'Light novel'), (95, 'Literary criticism'), (96, 'Literary fiction'), (97, 'Literary realism'), (98, 'Literary theory'), (99, 'Locked room mystery'), (100, 'Lost World'), (101, 'Low fantasy'), (102, 'Magic realism'), (103, 'Marketing'), (104, 'Mashup'), (105, 'Mathematics'), (106, 'Memoir'), (107, 'Metaphysics'), (108, 'Military history'), (109, 'Military science fiction'), (110, 'Modernism'), (111, 'Morality play'), (112, 'Music'), (113, 'Mystery'), (114, 'Nature'), (115, 'Naval adventure'), (116, 'Neuroscience'), (117, 'New Weird'), (118, 'New York Times Best Seller list'), (119, 'Non-fiction'), (120, 'Non-fiction novel'), (121, 'Novel'), (122, 'Novella'), (123, 'Parallel novel'), (124, 'Parody'), (125, 'Pastiche'), (126, 'Personal journal'), (127, 'Philosophy'), (128, 'Photography'), (129, 'Picaresque novel'), (130, 'Picture book'), (131, 'Play'), (132, 'Poetry'), (133, 'Polemic'), (134, 'Police procedural'), (135, 'Political philosophy'), (136, 'Politics'), (137, 'Popular culture'), (138, 'Popular science'), (139, 'Post-holocaust'), (140, 'Postcyberpunk'), (141, 'Postmodernism'), (142, 'Prose'), (143, 'Prose poetry'), (144, 'Psychological novel'), (145, 'Psychology'), (146, 'Reference'), (147, 'Religion'), (148, 'Robinsonade'), (149, 'Role-playing game'), (150, 'Roman à clef'), (151, 'Romance'), (152, 'Romantic comedy'), (153, 'Satire'), (154, 'School story'), (155, 'Science'), (156, 'Science Fiction'), (157, 'Science fantasy'), (158, 'Sea story'), (159, 'Self-help'), (160, 'Serial'), (161, 'Short story'), (162, 'Social commentary'), (163, 'Social criticism'), (164, 'Social novel'), (165, 'Social science fiction'), (166, 'Social sciences'), (167, 'Sociology'), (168, 'Soft science fiction'), (169, 'Space opera'), (170, 'Space western'), (171, 'Speculative fiction'), (172, 'Spirituality'), (173, 'Sports'), (174, 'Spy fiction'), (175, 'Steampunk'), (176, 'Subterranean fiction'), (177, 'Superhero fiction'), (178, 'Supernatural'), (179, 'Suspense'), (180, 'Sword and planet'), (181, 'Sword and sorcery'), (182, 'Techno-thriller'), (183, 'Thriller'), (184, 'Time travel'), (185, 'Tragicomedy'), (186, 'Transhumanism'), (187, 'Travel'), (188, 'Treatise'), (189, 'True crime'), (190, 'Urban fantasy'), (191, 'Urban fiction'), (192, 'Utopian and dystopian fiction'), (193, 'Utopian fiction'), (194, 'Vampire fiction'), (195, 'War novel'), (196, 'Western'), (197, 'Whodunit'), (198, 'Young adult literature'), (199, 'Youth'), (200, 'Zombie'))
class Browse(models.Model):
	title=models.TextField()
	author=models.TextField()
	genre=models.TextField()
	summary=models.TextField()
	

	def __str__(self):
		return self.title


class Preference(models.Model):
        date=models.DateTimeField(default=timezone.now)
        genre=MultiSelectField(choices=OPTIONS,blank=True)
        author=models.CharField(max_length=500,blank=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        
        def __str__(self):
                return str(self.date)

class Shelf(models.Model):
	date=models.DateTimeField(default=timezone.now)
	title=models.TextField()
	author=models.TextField()
	genre=models.TextField()
	summary=models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.title
	

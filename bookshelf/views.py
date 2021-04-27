from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Browse, Preference, Shelf
from .forms import PrefForm
from itertools import chain
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required

OPTIONS=((1, 'Absurdist fiction'), (2, 'Adventure'), (3, 'Adventure novel'), (4, 'Albino bias'), (5, 'Alien invasion'), (6, 'Alternate history'), (7, 'American Gothic Fiction'), (8, 'Anthology'), (9, 'Anthropology'), (10, 'Anti-nuclear'), (11, 'Anti-war'), (12, 'Apocalyptic and post-apocalyptic fiction'), (13, 'Autobiography'), (14, 'Bangsian fantasy'), (15, 'Bildungsroman'), (16, 'Biographical novel'), (17, 'Biography'), (18, 'Biopunk'), (19, 'Bit Lit'), (20, 'Black comedy'), (21, 'Boys school stories'), (22, 'Business'), (23, 'Cabal'), (24, 'Campus novel'), (25, 'Catastrophic literature'), (26, 'Chick lit'), (27, "Children's literature"), (28, 'Collage'), (29, 'Comedy'), (30, 'Comedy of manners'), (31, 'Comics'), (32, 'Coming of age'), (33, 'Computer Science'), (34, 'Conspiracy'), (35, 'Contemporary fantasy'), (36, 'Cookbook'), (37, 'Cozy'), (38, 'Creative nonfiction'), (39, 'Crime Fiction'), (40, 'Cyberpunk'), (41, 'Dark fantasy'), (42, 'Detective fiction'), (43, 'Drama'), (44, 'Dying Earth subgenre'), (45, 'Dystopia'), (46, 'Economics'), (47, 'Edisonade'), (48, 'Education'), (49, 'Encyclopedia'), (50, 'English public-school stories'), (51, 'Epic Science Fiction and Fantasy'), (52, 'Epistolary novel'), (53, 'Ergodic literature'), (54, 'Erotica'), (55, 'Essay'), (56, 'Existentialism'), (57, 'Experimental literature'), (58, 'Fable'), (59, 'Fairy tale'), (60, 'Fairytale fantasy'), (61, 'Fantastique'), (62, 'Fantasy'), (63, 'Fantasy of manners'), (64, 'Farce'), (65, 'Feminist science fiction'), (66, 'Fiction'), (67, 'Fictional crossover'), (68, 'Field guide'), (69, 'First-person narrative'), (70, 'Foreign legion'), (71, 'Future history'), (72, 'Gamebook'), (73, 'Ghost story'), (74, 'Gothic fiction'), (75, 'Graphic novel'), (76, 'Hard science fiction'), (77, 'Hardboiled'), (78, 'Heroic fantasy'), (79, 'High fantasy'), (80, 'Historical fantasy'), (81, 'Historical fiction'), (82, 'Historical novel'), (83, 'Historical whodunnit'), (84, 'History'), (85, 'Horror'), (86, 'Human extinction'), (87, 'Humour'), (88, 'Industrial novel'), (89, 'Inspirational'), (90, 'Invasion literature'), (91, 'Juvenile fantasy'), (92, 'Künstlerroman'), (93, 'LGBT literature'), (94, 'Light novel'), (95, 'Literary criticism'), (96, 'Literary fiction'), (97, 'Literary realism'), (98, 'Literary theory'), (99, 'Locked room mystery'), (100, 'Lost World'), (101, 'Low fantasy'), (102, 'Magic realism'), (103, 'Marketing'), (104, 'Mashup'), (105, 'Mathematics'), (106, 'Memoir'), (107, 'Metaphysics'), (108, 'Military history'), (109, 'Military science fiction'), (110, 'Modernism'), (111, 'Morality play'), (112, 'Music'), (113, 'Mystery'), (114, 'Nature'), (115, 'Naval adventure'), (116, 'Neuroscience'), (117, 'New Weird'), (118, 'New York Times Best Seller list'), (119, 'Non-fiction'), (120, 'Non-fiction novel'), (121, 'Novel'), (122, 'Novella'), (123, 'Parallel novel'), (124, 'Parody'), (125, 'Pastiche'), (126, 'Personal journal'), (127, 'Philosophy'), (128, 'Photography'), (129, 'Picaresque novel'), (130, 'Picture book'), (131, 'Play'), (132, 'Poetry'), (133, 'Polemic'), (134, 'Police procedural'), (135, 'Political philosophy'), (136, 'Politics'), (137, 'Popular culture'), (138, 'Popular science'), (139, 'Post-holocaust'), (140, 'Postcyberpunk'), (141, 'Postmodernism'), (142, 'Prose'), (143, 'Prose poetry'), (144, 'Psychological novel'), (145, 'Psychology'), (146, 'Reference'), (147, 'Religion'), (148, 'Robinsonade'), (149, 'Role-playing game'), (150, 'Roman à clef'), (151, 'Romance'), (152, 'Romantic comedy'), (153, 'Satire'), (154, 'School story'), (155, 'Science'), (156, 'Science Fiction'), (157, 'Science fantasy'), (158, 'Sea story'), (159, 'Self-help'), (160, 'Serial'), (161, 'Short story'), (162, 'Social commentary'), (163, 'Social criticism'), (164, 'Social novel'), (165, 'Social science fiction'), (166, 'Social sciences'), (167, 'Sociology'), (168, 'Soft science fiction'), (169, 'Space opera'), (170, 'Space western'), (171, 'Speculative fiction'), (172, 'Spirituality'), (173, 'Sports'), (174, 'Spy fiction'), (175, 'Steampunk'), (176, 'Subterranean fiction'), (177, 'Superhero fiction'), (178, 'Supernatural'), (179, 'Suspense'), (180, 'Sword and planet'), (181, 'Sword and sorcery'), (182, 'Techno-thriller'), (183, 'Thriller'), (184, 'Time travel'), (185, 'Tragicomedy'), (186, 'Transhumanism'), (187, 'Travel'), (188, 'Treatise'), (189, 'True crime'), (190, 'Urban fantasy'), (191, 'Urban fiction'), (192, 'Utopian and dystopian fiction'), (193, 'Utopian fiction'), (194, 'Vampire fiction'), (195, 'War novel'), (196, 'Western'), (197, 'Whodunit'), (198, 'Young adult literature'), (199, 'Youth'), (200, 'Zombie'))

##########################################################################################
def shelfToBrowse(l1):
        books=[]
        for book in list(l1):
                title=list(Browse.objects.filter(title=book.title))
                author=list(Browse.objects.filter(author=book.author))                
                books.append((list(set(title) & set(author)))[0])
        return books

'''def get_matches(search):
		if search.genre:
				checked_labels=[]     
				for tup in OPTIONS:
						if str(tup[0]) in list(search.genre):
							checked_labels.append(tup[1])

				gen=Browse.objects.filter(genre__contains=checked_labels[0])
				for x in range(1,len(checked_labels)):
						gn=Browse.objects.filter(genre__contains=checked_labels[x])
						gen=chain(gen,gn)
                
				gen=list(gen)
				auth=list(Browse.objects.filter(author__iexact=search.author))
				shelf=shelfToBrowse()
				gen=list(set(gen)-set(shelf))
				auth=list(set(auth)-set(shelf))
				both=list(set(auth)&set(gen))
				gen=list(set(gen)-set(both))
				auth=list(set(auth)-set(both))
				return (both,auth,gen)
        

		auth=list(Browse.objects.filter(author__iexact=search.author))
		return ([],auth,[])'''
	
def first_page(request):
        return render(request,"bookshelf/first_page.html")

@login_required(login_url='')
def home_page(request):
    return render(request, 'bookshelf/home_page.html', {})

def browse_books(request):
	books=Browse.objects.all().order_by('author')
	return render(request, 'bookshelf/browse_books.html', {'books':books})

def book_details(request,pk):
	book = get_object_or_404(Browse, pk=pk)
	return render(request, 'bookshelf/book_details.html', {'book': book})

def search_history(request):
        #searches=Preference.objects.all().order_by('-date')

        searches=Preference.objects.filter(user=request.user).order_by('-date')
        return render(request, 'bookshelf/search_history.html', {'searches':searches,'options':OPTIONS})

def make_search(request):
        if request.method == "POST":
                form = PrefForm(request.POST)
                if form.is_valid():
                        search = form.save(commit=False)
                        search.user=request.user
                        search.save()
                        if(search.genre or search.author):
                                checked_labels=[]
                                if search.genre:
                                        #print(search.genre)
                                        #checked_labels=[]     
                                        for tup in OPTIONS:
                                                if str(tup[0]) in list(search.genre):
                                                        checked_labels.append(tup[1])
                                        #print(checked_labels)

                                        gen=Browse.objects.filter(genre__contains=checked_labels[0])
                                        #print(gen)
                                        for x in range(1,len(checked_labels)):
                                                gn=Browse.objects.filter(genre__contains=checked_labels[x])
                                                #print("**************************************************")
                                                #print(gn)
                                                gen=list(chain(gen,gn))
                                                #print(gen)
                
                                        gen=list(gen)
                                        auth=list(Browse.objects.filter(author__iexact=search.author))
                                        #print(auth)
                                        shelf=shelfToBrowse(Shelf.objects.filter(user=request.user))
                                        #print(shelf)
                                        gen=list(set(gen)-set(shelf))
                                        auth=list(set(auth)-set(shelf))
                                        both=list(set(auth)&set(gen))
                                        gen=list(set(gen)-set(both))
                                        auth=list(set(auth)-set(both))
                                        matches=(both,auth,gen)
        

                                else:
                                        auth=list(Browse.objects.filter(author__iexact=search.author))
                                        matches=([],auth,[])
                                        

                

                                return render(request, 'bookshelf/matches.html', {'books': matches,'search':search,'checked_labels':checked_labels})#,'shelf':shelf})
                        else:
                                search.delete()
        else:
                form = PrefForm()
        return render(request, 'bookshelf/make_search.html', {'form': form})

def shelf_page(request):
        shelf_obj=Shelf.objects.filter(user=request.user).order_by('-date')
        books=shelfToBrowse(shelf_obj)
        return render(request, 'bookshelf/shelf_page.html', {'books': books})

def create_shelf_obj(request,pk):
        book = get_object_or_404(Browse, pk=pk)
        Shelf.objects.create(title=book.title, author=book.author, genre=book.genre, summary=book.summary, user=request.user)
        #search=Preference.objects.last(user=request.user)
        s=list(Preference.objects.filter(user=request.user))
        search=s[-1]

        checked_labels=[]
        if search.genre:
                #checked_labels=[]     
                for tup in OPTIONS:
                        if str(tup[0]) in list(search.genre):
                                checked_labels.append(tup[1])

                gen=Browse.objects.filter(genre__contains=checked_labels[0])
                for x in range(1,len(checked_labels)):
                        gn=Browse.objects.filter(genre__contains=checked_labels[x])
                        gen=chain(gen,gn)
                
                gen=list(gen)
                auth=list(Browse.objects.filter(author__iexact=search.author))
                shelf=shelfToBrowse(Shelf.objects.filter(user=request.user))
                gen=list(set(gen)-set(shelf))
                auth=list(set(auth)-set(shelf))
                both=list(set(auth)&set(gen))
                gen=list(set(gen)-set(both))
                auth=list(set(auth)-set(both))
                matches=(both,auth,gen)
        

        else:
                auth=list(Browse.objects.filter(author__iexact=search.author))
                matches=([],auth,[])
                                
                                        


        
        return render(request, 'bookshelf/matches.html', {'books': matches,'search':search, 'checked_labels':checked_labels})


#def del_shelf_obj():

#views to create user accts

def register(request):
	if request.method=="POST":
		form=UserCreationForm(request.POST)
		print(form.errors)
		if form.is_valid():
			form.save()
			return redirect("registered")
		else:
			return redirect("register")
	else:		
		return render(request,"bookshelf/register.html",{"form":UserCreationForm()})

def registered(request):
	return render(request,"bookshelf/registered.html")

class LoginView(View):
	def get(self,request):
		return render(request,"bookshelf/login.html",{"form":AuthenticationForm()})
	def post(self,request):
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			print ("login logic")
			user = authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))  #if usn and pwd match with inst in db
			print(user)
			if user is None:
				return redirect(request,"login.html",{"form":form,"invalid_creds":True})
			login(request, user)
			return redirect(reverse('home_page'))
			#return redirect('movies_list')
	
		else:
			print ("invalid login")
			return render(request,"login.html",{"form":form,"invalid_creds":True})

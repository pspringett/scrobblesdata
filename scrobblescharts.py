import os

from collections import namedtuple
from pprint import pprint
import dataclasses


@dataclasses.dataclass(order=True)
class TrackEntry:
    datetime: str
    artist: str
    album: str
    track: str


@dataclasses.dataclass(order=True)
class ChartEntry:
    key: str
    count: int
    previous_count: int
    gap: int
    isowned: str


@dataclasses.dataclass(order=True)
class SummaryEntry:
    total_tracks: int
    unique_artists: int
    unique_albums: int
    unique_tracks: int


compilations = {
    "soundtrack",
    "the story of trojan records",
    "30 years of punk",
    "a very special christmas",
    "50 of the greatest original xmas hits",
    "a tribute to gram parsons",
    "uncut",
    "crazy heart soundtrack",
    "nme c81",
    "tower of song - the songs of leonard cohen",
    "blowin' in the wind: a reggae tribute to bob dylan",
    "i'm not there",
    "eurovision song contest lisbon 2018",
    "rockers - original soundtrack",
}

myowned = {
    "* Naked As Advertised – Versions 08 - Heaven 17": 0,
    "007: The Best Of Desmond Dekker - Desmond Dekker \u0026 the Aces": 0,
    "16 Lovers Lane - The Go-Betweens": 0,
    "1969: The Velvet Underground Live With Lou Reed -- Volume 1 - The Velvet Underground": 0,
    "1969: The Velvet Underground With Lou Reed Live -- Volume 2 - The Velvet Underground": 0,
    "1978-1988 A Decade Of Spizz History - Spizz Energi": 0,
    "1981-2011 - B.E.F.": 0,
    "2010-06-10: Lafayette Square, Buffalo, Ny, Usa - Tift Merritt": 0,
    "2011-04-13: The Handlebar, Greenville, Sc, Usa - Hayes Carll": 0,
    "40 Days - The Wailin' Jennys": 1,
    "A Creature I Don't Know - Laura Marling": 0,
    "A Distant Shore - Tracey Thorn": 1,
    "A Friend Of A Friend - Dave Rawlings Machine": 0,
    "A Selection Of Songs - The French Impressionists": 0,
    "A Very Special Christmas 25th Anniversary - Various": 0,
    "A Word To The Wise Guy - The Mighty Wah!": 1,
    "A's, B's And Rarities - Suzi Quatro": 0,
    "Ablaze - School of Seven Bells": 0,
    "Achin In Yer Bones - Romi Mayes": 1,
    "Acoustic - Simple Minds": 0,
    "Acquaintance - Willie Nelson": 0,
    "Across The Atlantic - Sarah MacDougall": 1,
    "Alabama Song (International Version) - Allison Moorer": 0,
    "Aladdin Sane (2013 Remastered Version) - David Bowie": 0,
    "Aladdin Sane - David Bowie": 0,
    "Alas I Cannot Swim - Laura Marling": 1,
    "All Summer Long (2001 - Remaster) - The Beach Boys": 0,
    "All These Dreams - Andrew Combs": 0,
    "Altered Images 12 Inch Mix - Altered Images": 1,
    "American Kid - Patty Griffin": 0,
    "Anarchy In The UK - 30 Years Of Punk - Various": 1,
    "Anchors \u0026 Anvils - Amy LaVere": 1,
    "And The War Came - Shakey Graves": 0,
    "Andromeda Heights - Prefab Sprout": 1,
    "Another Country (International Edition) - Tift Merritt": 0,
    "Another Country - Tift Merritt": 0,
    "Another Green World - Brian Eno": 0,
    "Another View: A Collection Of Previously Unreleased Recordings - The Velvet Underground": 0,
    "Antidepressant - Lloyd Cole": 1,
    "Architecture \u0026 Morality - Live At The Royal Albert Hall 2016 - Orchestral Manoeuvres in the Dark": 1,
    "Architecture \u0026 Morality [Bonus Tracks] - Orchestral Manoeuvres in the Dark": 1,
    "Architecture And Morality - Orchestral Manoeuvres in the Dark": 1,
    "Architecture and Morality Live 2016 - Orchestral Manoeuvres in the Dark": 1,
    "Armed Forces - Elvis Costello \u0026 the Attractions": 0,
    "Ashes \u0026 Fire - Ryan Adams": 0,
    "Atlas - Real Estate": 0,
    "Back Home Again - John Denver": 0,
    "Bad Vibes - Lloyd Cole": 1,
    "Bang!... The Greatest Hits Of Frankie Goes To Hollywood - Frankie Goes to Hollywood": 0,
    "Barton Hollow - The Civil Wars": 0,
    "Beautiful World - Eliza Gilkyson": 1,
    "Before The Flood (Disc 1) - Bob Dylan": 1,
    "Before The Flood - Bob Dylan": 1,
    "Being Brave - Amanda Shires": 0,
    "Best Of - Middle of the Road": 0,
    "Beyond Leap - Martin Stephenson": 1,
    "Beyond The Leap Beyond The Law - Martin Stephenson": 1,
    "Birds Of Chicago - Birds of Chicago": 1,
    "Bite - Altered Images": 1,
    "Black Cadillac - Rosanne Cash": 1,
    "Black Eyed Man - Cowboy Junkies": 1,
    "Blackbirds - Gretchen Peters": 1,
    "Blonde On Blonde - Bob Dylan": 1,
    "Blood On The Tracks - Bob Dylan": 1,
    "Boat To Bolivia - Martin Stephenson and the Daintees": 1,
    "Bob Dylan At Budokan (Cd1) - Bob Dylan": 0,
    "Bob Dylan At Budokan - Bob Dylan": 1,
    "Boy - U2": 1,
    "Bramble Rose - Tift Merritt": 0,
    "Breakout - Louisa Mark": 0,
    "Brigid Mae Power - Brigid Mae Power": 0,
    "Bringing It All Back Home - Bob Dylan": 1,
    "Broken Carelessly - The Redlands Palomino Company": 1,
    "Broken Record - Lloyd Cole": 1,
    "Buckingham Solo - Tift Merritt": 0,
    "Burnin' - Bob Marley": 0,
    "Burnin' - The Wailers": 0,
    "Butcher Holler - A Tribute To Loretta Lynn - Eilen Jewell": 1,
    "By the Time You Hear This ...We'll Be Gone - The Redlands Palomino Company": 1,
    "Cabin Fever (Cabin Side) - Corb Lund": 1,
    "Cabin Fever (Fever Side) - Corb Lund": 1,
    "Cabin Fever - Corb Lund": 1,
    "Cafe Bleu - The Style Council": 0,
    "Caledonia - JT and the Clouds": 1,
    "California Star - Martin Stephenson and the Daintees": 1,
    "Candleland - Ian McCulloch": 1,
    "Car Wheels On A Gravel Road - Lucinda Williams": 1,
    "Carrie \u0026 Lowell - Sufjan Stevens": 0,
    "Carrying Lightning - Amanda Shires": 0,
    "Case/lang/veirs - case/lang/veirs": 0,
    "Catch A Fire (Deluxe Edition) - Bob Marley \u0026 the Wailers": 0,
    "Celebration - Simple Minds": 0,
    "Celilo Falls - Rachel Harrington": 1,
    "Chaleur Humaine - Christine and the Queens": 0,
    "Changesonebowie - David Bowie": 0,
    "Children Running Through - Patty Griffin": 1,
    "Christie - Christie": 0,
    "Christmas - The Collection (50 Of The Greatest Original Xmas Hits) - Various": 0,
    "City Of Refuge - Rachel Harrington": 1,
    "Cleaning Out The Ashtrays CD1 - One Red Wine Glass - Lloyd Cole": 1,
    "Cleaning Out The Ashtrays CD2 - Re-make/Re-model - Lloyd Cole": 1,
    "Cleaning Out The Ashtrays CD3 - Dangerous Music - Lloyd Cole": 1,
    "Cleaning Out The Ashtrays CD4 - Dificult Pieces - Lloyd Cole": 1,
    "Close To The Bone - Bonus - Tom Tom Club": 0,
    "Close To The Bone - Tom Tom Club": 0,
    "Closer - Joy Division": 1,
    "Closing Time - Tom Waits": 0,
    "Collected Recordings 1983-1989 - Lloyd Cole and the Commotions": 0,
    "Colossal Youth - Young Marble Giants": 0,
    "Counterfeit Blues - Corb Lund": 0,
    "Country Life - Roxy Music": 0,
    "Crazy Heart Soundtrack - Various": 1,
    "Crows - Allison Moorer": 0,
    "Darling Arithmetic (Deluxe Version) - Villagers": 0,
    "David Bowie - Bonus - David Bowie": 1,
    "David Bowie - David Bowie": 1,
    "David Rodigan Summmer Of Reggae - David Rodigan": 1,
    "Dazzle Ships (Remastered) - Orchestral Manoeuvres in the Dark": 1,
    "Dazzle Ships - Live At The Royal Albert Hall 2016 - Orchestral Manoeuvres in the Dark": 1,
    "Dazzle Ships Live 2016 - Orchestral Manoeuvres in the Dark": 1,
    "Dazzle Ships Live At The Museum Of Liverpool - Orchestral Manoeuvres in the Dark": 1,
    "Demons - JT Nero": 1,
    "Demons/Demons - JT Nero": 1,
    "Departure And Farewell - Hem": 1,
    "Desire - Bob Dylan": 1,
    "Diamond Dogs (30th Anniversary Edition) - David Bowie": 0,
    "Dire Straits (Remastered) - Dire Straits": 0,
    "Don't Fade - The Redlands Palomino Company": 1,
    "Don't Get Weird On Me Babe - Lloyd Cole": 1,
    "Down To Believing - Allison Moorer": 0,
    "Drumming The Beating Heart - Eyeless in Gaza": 0,
    "Duran Duran - Duran Duran": 0,
    "Easy Pieces (Remastered 2015) - Lloyd Cole and the Commotions": 1,
    "Echo \u0026 The Bunnymen (Expanded \u0026 Remastered) - Echo \u0026 the Bunnymen": 0,
    "Electric Warrior (Deluxe Edition) - T. Rex": 0,
    "Electric Warrior - T. Rex": 1,
    "Empire Burlesque (Remastered) - Bob Dylan": 1,
    "Empire Burlesque - Bob Dylan": 1,
    "Epic Recordings - Shelby Lynne": 0,
    "Essential Music Hits Vol 2 - Mike Oldfield": 0,
    "Essential Reggae - 20 Reggae Classics - Sugar Minott": 0,
    "Eveningland - Hem": 1,
    "Excellent Day - Lizanne Knott": 0,
    "Exodus Of Venus - Elizabeth Cook": 0,
    "Faith - The Cure": 1,
    "Far Away In Time - Martha and the Muffins": 0,
    "Fate's Right Hand - Rodney Crowell": 1,
    "Feels Like Home - Sheryl Crow": 0,
    "Firecracker - The Wailin' Jennys": 1,
    "For Your Pleasure - Roxy Music": 0,
    "Fossils - Aoife O'Donovan": 0,
    "From Langley Park To Memphis - Prefab Sprout": 1,
    "Funnel Cloud (Bonus Track Version) - Hem": 1,
    "GRRR! - The Rolling Stones": 0,
    "Get Happy - Bonus - Elvis Costello \u0026 the Attractions": 1,
    "Get Happy!! - Elvis Costello \u0026 the Attractions": 1,
    "Get Up (Deluxe) - Bryan Adams": 0,
    "Girls In Peacetime Want To Dance - Belle and Sebastian": 0,
    "Gladsome, Humour \u0026 Blue - Martin Stephenson and the Daintees": 1,
    "Golden Apples Of The Sun - Caroline Herring": 0,
    "Golden Oldies - Focus": 0,
    "Good As I Been To You (Remastered) - Bob Dylan": 0,
    "Goodbye Yellow Brick Road (40th Anniversary Celebration) - Elton John": 0,
    "Goodnight City - Martha Wainwright": 0,
    "Gorgeous George - Edwyn Collins": 1,
    "Grand Canyon - Sarah MacDougall": 1,
    "Grand Canyon Early Release - Sarah MacDougall": 1,
    "Greatest Hits (International Version) - Shania Twain": 0,
    "Greatest Hits - Slade": 0,
    "Greatest Hits Of Nick Heyward + Haircut 100 - Haircut 100": 0,
    "Greatest Hits Of Nick Heyward + Haircut 100 - Nick Heyward": 0,
    "Greatest Hits: Brotherhood Of Man - Brotherhood of Man": 0,
    "Grrr! - The Rolling Stones": 0,
    "Ha! Ha! Ha! - Ultravox": 0,
    "Hair In My Eyes Like A Highland Steer - Corb Lund": 1,
    "Happy Birthday - Altered Images": 1,
    "Happy Together - The Turtles": 0,
    "Hard Rain - Bob Dylan": 1,
    "Harlem River Blues - Justin Townes Earle": 1,
    "Have You In My Wilderness - Julia Holter": 0,
    "Head Over Heels - Cocteau Twins": 0,
    "Heartbeat - Rudy Thomas": 0,
    "Heaven Up Here - Echo \u0026 the Bunnymen": 1,
    "Hellbent On Compromise - Edwyn Collins": 1,
    "Hello Cruel World - Gretchen Peters": 0,
    "Helplessness Blues - Fleet Foxes": 0,
    "Here We Rest - Jason Isbell and the 400 Unit": 0,
    "Heroes - David Bowie": 1,
    "High 7 Moon 5 - Martin Stephenson": 1,
    "High Land, Hard Rain - Aztec Camera": 1,
    "Highway 61 Revisited - Bob Dylan": 1,
    "Hold Yer Horses - The Piney Gir Country Roadshow": 0,
    "Honky Chateau (Remastered) - Elton John": 0,
    "Hope And Despair - Edwyn Collins": 1,
    "Horse Soldier! Horse Soldier! - Corb Lund": 1,
    "I Am Shelby Lynne (Bonus Track Version) - Shelby Lynne": 0,
    "I Can't Imagine - Shelby Lynne": 0,
    "I Heard It Through The Grapevine / In The Groove (Stereo) - Marvin Gaye": 0,
    "I Speak Because I Can - Laura Marling": 1,
    "I Took Up The Runes - Jan Garbarek": 1,
    "I'd Rather Go Blind - Single - the FRIGHTNRS": 0,
    "I'm In Love With A German Film Star - The Passions": 0,
    "I'm Not Following You - Edwyn Collins": 1,
    "I'm Your Man - Leonard Cohen": 1,
    "Identity Crisis - Shelby Lynne": 0,
    "Imagination Feels Like Poison - Martyn Bates": 1,
    "Imagine - Joan Baez": 0,
    "Imperial Bedroom - Elvis Costello \u0026 the Attractions": 0,
    "Impossible Dream - Haley Bonar": 0,
    "Impossible Dream - Patty Griffin": 1,
    "In City And In Forest - Tower of Song": 0,
    "In Time - The Mavericks": 0,
    "Infidels (Remastered 2003) - Bob Dylan": 1,
    "Introducing The Style Council - The Style Council": 0,
    "It's Immaterial - Black Marble": 0,
    "Jessica Pratt - Jessica Pratt": 0,
    "Jordan: The Comeback - Prefab Sprout": 1,
    "Journeys To Glory (2010 - Remaster) - Spandau Ballet": 0,
    "Journeys To Glory (Special Edition) - Spandau Ballet": 0,
    "Junk Culture (Deluxe Edition) - Orchestral Manoeuvres in the Dark": 0,
    "Junk Culture - Orchestral Manoeuvres in the Dark": 0,
    "Just A Little Lovin' - Shelby Lynne": 0,
    "King Of America - Elvis Costello": 0,
    "Kmag Yoyo (\u0026 Other American Stories) - Hayes Carll": 1,
    "Knife - Aztec Camera": 1,
    "Knife Extended - Aztec Camera": 1,
    "Last Christmas - Wham!": 0,
    "Lay It Down - Cowboy Junkies": 1,
    "Learning To Crawl - The Pretenders": 0,
    "Led Zeppelin - Led Zeppelin": 1,
    "Let's Dance - David Bowie": 0,
    "Letters From Sinners \u0026 Strangers - Eilen Jewell": 1,
    "Letters To Sinners \u0026 Strangers - Eilen Jewell": 1,
    "Liberator - Orchestral Manoeuvres in the Dark": 1,
    "Liberty Belle And The Black Diamond Express - The Go-Betweens": 0,
    "Life On Mars Original Soundtrack - Various": 1,
    "Life's Hard And Then You Die - It's Immaterial": 0,
    "Little Creatures - Talking Heads": 1,
    "Little Neon Limelight - Houndmouth": 0,
    "Little Rock - Hayes Carll": 1,
    "Live At Blue Rock - Mary Gauthier": 0,
    "Live At Brooklyn Bowl 2016 - Lloyd Cole": 1,
    "Live At Eddie's Attic - The Civil Wars": 0,
    "Live At The Narrows - Eilen Jewell": 0,
    "Live At Union Chapel 2016 - Lloyd Cole": 1,
    "Live From KXLU Radio - Gina Villalobos": 1,
    "Live From Kxlu Radio - Gina Villalobos": 1,
    "Live From Space - Birds of Chicago": 0,
    "Live In Louisville - Carrie Rodriguez": 1,
    "Live at Brooklyn Bowl 2016 - Lloyd Cole": 1,
    "Live at Union Chapel 2016 - Lloyd Cole": 1,
    "Lloyd Cole - Lloyd Cole": 1,
    "Lloyd Cole Small Ensemble Slaughterhouse Studios 01-22-2010 - Lloyd Cole": 1,
    "Look - Beth Nielsen Chapman": 0,
    "Losing Sleep - Edwyn Collins": 1,
    "Lost And Found - Eliza Gilkyson": 1,
    "Lost On The River (Deluxe Edition) - The New Basement Tapes": 0,
    "Love - Aztec Camera": 0,
    "Love And Circumstance - Carrie Rodriguez": 1,
    "Love And Theft - Bob Dylan": 0,
    "Love Story - Lloyd Cole": 1,
    "Love This Giant - David Byrne \u0026 St. Vincent": 0,
    "Love What You Do - Hackensaw Boys": 0,
    "Lovers And Leavers - Hayes Carll": 0,
    "Low - David Bowie": 0,
    "Mainstream - Lloyd Cole and the Commotions": 0,
    "Manifesto - Roxy Music": 0,
    "Marcus Garvey: The Best Of Burning Spear - Burning Spear": 0,
    "Mccartney II (Special Edition) - Paul McCartney": 1,
    "Mccartney Ii (Special Edition) - Paul McCartney": 0,
    "Meanwhile, As Night Falls... - Angie Palmer": 1,
    "Melophobia - Cage the Elephant": 0,
    "Memorial Album - Don Drummond \u0026 the Skatalites": 0,
    "Merry Christmas Wherever You Are - George Strait": 0,
    "Merry Christmas, Baby - Rod Stewart": 0,
    "Midwest Farmer's Daughter - Margo Price": 0,
    "Modern Blues - The Waterboys": 0,
    "Modern Times - Bob Dylan": 0,
    "Mono - The Mavericks": 0,
    "More Than Somewhat: The Very Best Of - Steve Harley \u0026 Cockney Rebel": 0,
    "More Than This: The Best Of Bryan Ferry + Roxy Music - Roxy Music": 0,
    "Mountains/Forests - JT Nero": 1,
    "Movement [Collector's Edition] - New Order": 1,
    "Music For Sixties - Manfred Mann": 0,
    "My Favorite Picture Of You - Guy Clark": 0,
    "My Life In The Bush Of Ghosts - Brian Eno \u0026 David Byrne": 1,
    "My Piece Of Land - Amanda Shires": 0,
    "Naked as Advertised - Version 08 - Heaven 17": 0,
    "Nashville Obsolete - Dave Rawlings Machine": 0,
    "Natalie Prass - Natalie Prass": 0,
    "National Ransom - Elvis Costello": 0,
    "New Gold Dream (81-82-83-84) - Simple Minds": 1,
    "New Skin For The Old Ceremony - Leonard Cohen": 0,
    "Night - Tift Merritt": 0,
    "No Regrets: The Best Of Scott Walker \u0026 The Walker Brothers - The Walker Brothers": 0,
    "No Way There From Here - Laura Cantrell": 0,
    "No Word From Tom (Bonus Track Version) - Hem": 1,
    "No Word From Tom - Hem": 1,
    "Noel Inoubliable - Frank Sinatra": 0,
    "North Star - Roddy Frame": 1,
    "Nothing But The Silence - Striking Matches": 0,
    "Nothing's Gonna Change The Way You Feel About Me Now - Justin Townes Earle": 0,
    "Noël Inoubliable - Frank Sinatra": 0,
    "Ocean Rain (Expanded \u0026 Remastered) - Echo \u0026 the Bunnymen": 0,
    "Ocean Rain - Echo \u0026 the Bunnymen": 1,
    "Oceans - Artery": 0,
    "October - U2": 1,
    "Ogden's Nut Gone Flake - Small Faces": 0,
    "Oh My God, Charlie Darwin - The Low Anthem": 1,
    "Old Ideas - Leonard Cohen": 0,
    "Old Sticks To Scare A Bird - Angie Palmer": 1,
    "Old Yellow Moon - Emmylou Harris": 0,
    "On My Heart - School of Seven Bells": 0,
    "Once Upon A Christmas - Dolly Parton": 0,
    "One Moment More - Mindy Smith": 1,
    "One To The Heart, One To The Head - Gretchen Peters": 0,
    "Only Yazoo - The Best Of Yazoo - Yazoo": 0,
    "Ooh La La - Faces": 0,
    "Open Your Eyes - School of Seven Bells": 0,
    "Orchestral Manoeuvres In The Dark - Orchestral Manoeuvres in the Dark": 1,
    "Organisation - Orchestral Manoeuvres in the Dark": 1,
    "Our Favourite Shop (Digitally Remastered) - The Style Council": 0,
    "Outlandos D'amour (Remastered) - The Police": 0,
    "Pacific Street - The Pale Fountains": 0,
    "Pageant Material - Kacey Musgraves": 0,
    "Paging Mr. Proust - The Jayhawks": 0,
    "Paris 1919 (Remastered + Expanded) - John Cale": 1,
    "Pat Garrett \u0026 Billy The Kid [Soundtrack] - Various": 1,
    "Peace At Last - EP - Hem": 0,
    "Peace At Last - Ep - Hem": 0,
    "Peaceful, The World Lays Me Down - Noah and the Whale": 0,
    "Pelican West Plus - Haircut 100": 0,
    "Penthouse And Pavement (Special Edition) - B.E.F.": 0,
    "Penthouse And Pavement (Special Edition) - Heaven 17": 0,
    "Penthouse And Pavement - Heaven 17": 0,
    "Penthouse and Pavement (Special Edition) - Heaven 17": 0,
    "Pet Sounds - 40th Anniversary - The Beach Boys": 0,
    "Pin Ups - David Bowie": 0,
    "Pinky Blue - Altered Images": 1,
    "Pinups (2015 Remastered Version) - David Bowie": 0,
    "Pinups - David Bowie": 0,
    "Plastic Wood - Lloyd Cole": 1,
    "Platinum - Miranda Lambert": 0,
    "Please Please Me (Remastered) - The Beatles": 0,
    "Popera: The Singles Collection - The Associates": 1,
    "Popular Problems - Leonard Cohen": 0,
    "Population: Me - Dwight Yoakam": 0,
    "Porcupine - Echo \u0026 the Bunnymen": 0,
    "Pornography - The Cure": 1,
    "Positive Touch - The Undertones": 0,
    "Postcard Singles - Josef K": 1,
    "Power To The People: The Hits - John Lennon": 0,
    "Power, Corruption \u0026 Lies - New Order": 1,
    "Power, Corruption \u0026 Lies [Collector's Edition] - New Order": 1,
    "Protest Songs - Prefab Sprout": 0,
    "Psychocandy - The Jesus and Mary Chain": 0,
    "Punch The Clock - Elvis Costello \u0026 the Attractions": 0,
    "Pure... Christmas - Greg Lake": 0,
    "Queen Of The Minor Key - Eilen Jewell": 1,
    "Quite A Feelin' - Barna Howard": 0,
    "Rabbit Songs - Hem": 1,
    "Rain Dogs - Tom Waits": 0,
    "Raising Sand - Robert Plant \u0026 Alison Krauss": 1,
    "Rattlesnakes (Deluxe Edition) - Lloyd Cole and the Commotions": 1,
    "Rattlesnakes (Remastered 2015) - Lloyd Cole and the Commotions": 1,
    "Rattlesnakes - Lloyd Cole and the Commotions": 1,
    "Reading, Writing \u0026 Arithmetic - The Sundays": 1,
    "Red Dirt Girl - Emmylou Harris": 0,
    "Red Dog Tracks - Chip Taylor": 1,
    "Redshift - Rhyton": 0,
    "Remain In Light (Deluxe Version) - Talking Heads": 1,
    "Remain In Light - Talking Heads": 1,
    "Replicas - Gary Numan": 0,
    "Resonator - Kathryn Williams, Anthony Kerr": 0,
    "Return of the Grievous Angel: A Tribute to Gram Parsons - Various": 1,
    "Revelation Road (Deluxe Version) - Shelby Lynne": 0,
    "Revelation Road - Shelby Lynne": 0,
    "Revival - Gillian Welch": 0,
    "Rip It Up - Orange Juice": 0,
    "Road - Angie Palmer": 1,
    "Rock N Roll Jamboree - Stephenson's Rocketts": 1,
    "Rock Your Baby: The Best Of George Mccrae - George McCrae": 0,
    "Rockers - Original Soundtrack - Various": 1,
    "Roxy Music - Roxy Music": 1,
    "Rules Of Travel - Rosanne Cash": 0,
    "SVIIB - School of Seven Bells": 0,
    "Same Trailer Different Park - Kacey Musgraves": 0,
    "Santa Claus Is Comin' To Town - Bruce Springsteen": 0,
    "Saturns Pattern - Paul Weller": 0,
    "Saved - Bob Dylan": 1,
    "Scheherazade - Freakwater": 0,
    "Scott - Scott Walker": 1,
    "Scott 2 - Scott Walker": 1,
    "Script Of The Bridge (Remastered) - The Chameleons": 0,
    "Script Of The Bridge - 25th Anniversary Edition - The Chameleons": 0,
    "Sea Of Tears - Eilen Jewell": 1,
    "Second Flight - Pilot": 0,
    "Second Sight - Corinne West": 1,
    "See You Around - Travis Linville": 1,
    "See You On The Moon (Digital Ebooklet) - Tift Merritt": 0,
    "See You On The Moon - Tift Merritt": 0,
    "Servant Of Love - Patty Griffin": 0,
    "Seven Angels On A Bicycle - Carrie Rodriguez": 1,
    "Seven Dials - Roddy Frame": 1,
    "Seventeen Seconds (Remastered Version) - The Cure": 1,
    "Seventeen Seconds - The Cure": 1,
    "Sew Your Heart With Wires - Rod Picott \u0026 Amanda Shires": 1,
    "Sew Your Heart With Wires - Rod Picott and Amanda Shires": 1,
    "Sextet - A Certain Ratio": 0,
    "She Ain't Me - Carrie Rodriguez": 1,
    "Shot Of Love - Bob Dylan": 1,
    "Side By Side (Live At Spacebomb Studios) - Natalie Prass": 0,
    "Signing Off - UB40": 1,
    "Single Mothers - Justin Townes Earle": 0,
    "Singles - New Order": 0,
    "Slow Gum - Fraser A. Gorman": 0,
    "Slow Train Coming - Bob Dylan": 1,
    "Small Change - Tom Waits": 0,
    "Smile (Expanded Edition) - The Jayhawks": 0,
    "Snap - The Jam": 1,
    "Snap, Crackle \u0026 Bop - John Cooper Clarke": 0,
    "Solitude Standing - Suzanne Vega": 0,
    "Something More Than Free - Jason Isbell": 0,
    "Something On My Mind - The Pale Fountains": 0,
    "Song To A Seagull - Joni Mitchell": 0,
    "Songs - John Fullbright": 0,
    "Songs From A Room - Leonard Cohen": 1,
    "Songs Of Leonard Cohen - Leonard Cohen": 1,
    "Songs Of Love And Hate - Leonard Cohen": 0,
    "Songs To Learn And Sing - Echo \u0026 the Bunnymen": 0,
    "Songs To Play - Robert Forster": 0,
    "Songs To Remember - Scritti Politti": 1,
    "Sons And Fascination/sister Feelings Call - Simple Minds": 1,
    "Soul Journey - Gillian Welch": 1,
    "Sound Affects (Remastered Version) - The Jam": 0,
    "Southside - Texas": 1,
    "Sparkle In The Rain - Simple Minds": 1,
    "Speaking In Tongues (Deluxe Version) - Talking Heads": 0,
    "Springtime - Freakwater": 0,
    "Stage - David Bowie": 0,
    "Standards - Lloyd Cole": 1,
    "Station To Station - David Bowie": 1,
    "Station To Station [Special Edition] - David Bowie": 1,
    "Stealers Wheel - Stealers Wheel": 0,
    "Steve McQueen - Prefab Sprout": 1,
    "Stop Making Sense - Talking Heads": 1,
    "Stop Making Sense [Special Edition] - Talking Heads": 1,
    "Stop The Cavalry - Jona Lewie": 0,
    "Stranded - Roxy Music": 0,
    "Strange Angels - Kristin Hersh": 0,
    "Stranger Me - Amy LaVere": 0,
    "Street Legal - Bob Dylan": 1,
    "Stumble Into Grace - Emmylou Harris": 1,
    "Sub-Stance - Department S": 0,
    "Sub-stance - Department S": 0,
    "Substance 1987 - New Order": 0,
    "Suit Yourself - Shelby Lynne": 0,
    "Sundown Over Ghost Town - Eilen Jewell": 0,
    "Suzanne Vega - Suzanne Vega": 0,
    "Sweet Somethin' Steady - Romi Mayes": 1,
    "Swoon - Prefab Sprout": 1,
    "Take Me Home - The Redlands Palomino Company": 0,
    "Tales Of Light \u0026 Darkness - Angie Palmer": 1,
    "Tales Of Light And Darkness - Angie Palmer": 1,
    "Tallulah - The Go-Betweens": 1,
    "Tambourine - Tift Merritt": 0,
    "Tangled - Nick Heyward": 0,
    "Tarpaper Sky - Rodney Crowell": 0,
    "Tears, Lies And Alibis - Shelby Lynne": 0,
    "Tempting The Storm - Cara Luft": 0,
    "Texas Fever - Orange Juice": 1,
    "The '81 Demos - Weekend": 0,
    "The 70's Studio Album Collection - Emmylou Harris": 0,
    "The Avenues - Lera Lynn": 0,
    "The BBC Sessions - Loudon Wainwright III": 1,
    "The Best Of - Joy Division": 0,
    "The Best Of - Nick Cave \u0026 the Bad Seeds": 0,
    "The Best Of - The Staple Singers": 0,
    "The Best Of David Bowie, '69-'74 - David Bowie": 0,
    "The Best Of Siouxsie And The Banshees - Siouxsie and the Banshees": 0,
    "The Boatman's Call - Nick Cave \u0026 the Bad Seeds": 0,
    "The Bootlegger's Daughter - Rachel Harrington": 1,
    "The Caution Horses - Cowboy Junkies": 1,
    "The Church And The Minidisc - Martin Stephenson": 1,
    "The City's Hot Yeah The City's Hot - JT and the Clouds": 1,
    "The Collection - Altered Images": 1,
    "The Complete Matrix Tapes - The Velvet Underground": 0,
    "The Complete Peel Sessions 1978-2004 - The Fall": 0,
    "The Cutting Edge 1965-1966: The Bootleg Series, Vol. 12 (Sampler) - Bob Dylan": 0,
    "The Essential Leonard Cohen - Leonard Cohen": 0,
    "The Essential Mindy Smith - Mindy Smith": 0,
    "The Future - Leonard Cohen": 0,
    "The Glasgow School - Orange Juice": 0,
    "The Grass Is Blue - Dolly Parton": 1,
    "The Greatest Ones Alive - Sarah MacDougall": 1,
    "The Joshua Tree (Remastered) - U2": 0,
    "The Joshua Tree - U2": 0,
    "The King Is Dead - The Decemberists": 1,
    "The Lexicon Of Love (Digitally Remastered) - ABC": 0,
    "The Light Fantastic - Cara Luft": 1,
    "The List - Rosanne Cash": 0,
    "The Magic 0f Christmas - Nat King Cole": 0,
    "The Man Who Sold The World - David Bowie": 1,
    "The Modern Lovers - Jonathan Richman and the Modern Lovers": 0,
    "The Monkees Collection - The Monkees": 1,
    "The Negatives - Lloyd Cole": 1,
    "The New Bye \u0026 Bye - Chip \u0026 Carrie": 0,
    "The North Star - Roddy Frame": 1,
    "The Orange Juice - Orange Juice": 1,
    "The Outsider - Rodney Crowell": 0,
    "The Outsider - Rodney Crowell (Duet With Emmylou Harris)": 0,
    "The Pink Opaque - Cocteau Twins": 0,
    "The Prince Of Wales - Devine \u0026 Statton": 0,
    "The Rise And Fall Of Ziggy Stardust And The Spiders From Mars (2012 Remastered Version) - David Bowie": 0,
    "The Rise And Fall Of Ziggy Stardust And The Spiders From Mars [30th Anniversary Edition] - David Bowie": 1,
    "The River \u0026 The Thread (Deluxe) - Rosanne Cash": 0,
    "The River \u0026 The Thread - Rosanne Cash": 0,
    "The Sin Of Pride - The Undertones": 0,
    "The Singles - Soft Cell": 0,
    "The Smiths - The Smiths": 0,
    "The Story Of Trojan Records - Various": 0,
    "The T.Rex Wax Co. Singles A's \u0026 B's 1972-77 - T. Rex": 1,
    "The Things That We Are Made Of - Mary Chapin Carpenter": 0,
    "The Trinity Session - Cowboy Junkies": 1,
    "The Trojan: Rocksteady Collection - Alton Ellis": 0,
    "The Unforgettable Fire - U2": 1,
    "The Very Best Of - Orange Juice": 0,
    "The Wrong People - Furniture": 0,
    "Themes - Volume 2 - Simple Minds": 0,
    "There Comes A Time - Martin Stephenson and the Daintees": 1,
    "There Goes Concorde Again - Native Hipsters": 0,
    "Thick As Thieves - Larkin Poe": 1,
    "This Year's Model - Bonus - Elvis Costello \u0026 the Attractions": 1,
    "This Year's Model - Elvis Costello \u0026 the Attractions": 1,
    "This Year's Model - Live 1978 - Elvis Costello \u0026 the Attractions": 1,
    "Time Out Of Mind - Bob Dylan": 0,
    "Tin Drum - Japan": 0,
    "Tom Tom Club - Tom Tom Club": 1,
    "Tom Tom Club Bonus - Tom Tom Club": 0,
    "Top 100 80s - New Order": 0,
    "Tower Of Song - The Songs Of Leonard Cohen - Various": 0,
    "Town \u0026 Country - The Vagaband": 0,
    "Transformer - Lou Reed": 1,
    "Traveling Alone - Tift Merritt": 0,
    "Traveling Companion - Tift Merritt": 0,
    "Treasure - Cocteau Twins": 0,
    "Trinity Revisited - Cowboy Junkies": 0,
    "Trouble In Mind - Hayes Carll": 1,
    "Tusk - Fleetwood Mac": 1,
    "UNCUT 2016-02 - What's Going On! - Various": 1,
    "UNCUT 2016-03 - The Stars Are Out Tonight - Various": 1,
    "UNCUT 2016-04 - On The Highway - Various": 1,
    "UNCUT 2016-05 - Let Uncut Shake - Various": 1,
    "UNCUT 2016-06 - Picture This - Various": 1,
    "UNCUT 2016-08 - The Goldrush - Various": 1,
    "UNCUT 2016-09 - Ones From The Heart - Various": 1,
    "UNCUT 2016-11 - Sterotypes - Various": 1,
    "UNCUT 2016-12 - The Hustle - Various": 1,
    "Ultimate Waylon Jennings - Waylon Jennings": 0,
    "Under Branch \u0026 Thorn \u0026 Tree - Samantha Crain": 0,
    "Undercurrent - Sarah Jarosz": 0,
    "Unknown Album - Cowboy Junkies": 1,
    "Unknown Album - M. Ward": 0,
    "Unknown Album - Natural Child": 0,
    "Unknown Album - Rokia Traoré": 0,
    "Unknown Pleasures - Joy Division": 1,
    "Unplugged... And Seated - Rod Stewart": 1,
    "Upstairs At Erics (Remastered) - Yazoo": 0,
    "Utah - Jamestown Revival": 0,
    "VH1 Storytellers - David Bowie": 0,
    "Van Lear Rose - Loretta Lynn": 1,
    "Various Positions - Leonard Cohen": 1,
    "Vh1 Storytellers - David Bowie": 0,
    "War - U2": 0,
    "We Still Love Our Country - Carrie Rodriguez and Ben Kyle": 1,
    "Welcome To Scullyville - Martin Stephenson": 1,
    "Western Skies - Roddy Frame": 0,
    "What A Terrible World, What A Beautiful World - The Decemberists": 0,
    "When The Roses Bloom Again - Laura Cantrell": 0,
    "Who Can I Be Now? [1974 - 1976] - David Bowie": 0,
    "Wilder (Remastered Expanded Edition) - The Teardrop Explodes": 0,
    "Wilder - The Teardrop Explodes": 0,
    "Willie And The Wheel - Willie Nelson \u0026 Asleep At the Wheel": 1,
    "Wishful Thinking: The Very Best Of China Crisis - China Crisis": 0,
    "With The Beatles (Remastered) - The Beatles": 0,
    'Words (Music From The Film "tig") - Sharon Van Etten': 0,
    "Work, Pt. 1 - Walter Salas-Humara": 0,
    "World At Large - The Dust Poets": 1,
    "World Gone Wrong (Remastered) - Bob Dylan": 0,
    "Wouldn't You Like It - Bay City Rollers": 0,
    "Wrecking Ball - Emmylou Harris": 1,
    "Yogi In My House - Martin Stephenson": 1,
    "You And Me Both - Yazoo": 0,
    "You Can't Hide Your Love Forever - Orange Juice": 0,
    "You Want It Darker - Leonard Cohen": 0,
    "You and Me Both - Yazoo": 0,
    "Young Americans - David Bowie": 1,
    "Young In All The Wrong Ways - Sara Watkins": 0,
}


def make_chart(tracks, key_type):

    unsorted_chart = {}
    for track in tracks:
        # print("Track={}".format(track))
        entry = TrackEntry(track[0], track[1], track[2], track[3])

        if key_type == "album":
            if entry.album.lower() in compilations:
                entry.artist = "Various"

        key = get_key(key_type, entry.artist, entry.album, entry.track)
        # print("key={}".format(key))

        if key not in unsorted_chart:
            chart_entry = ChartEntry(key, 0, 0, 0, "-")
            unsorted_chart[key] = chart_entry

        unsorted_chart[key].count += 1
        unsorted_chart[key].previous_count += 1

        try:
            isowned = myowned[key] == 1
        except:
            isowned = False

        if isowned:
            unsorted_chart[key].isowned = "*"

    # pprint(basic_chart, indent=4)
    chart = list(dict.values(unsorted_chart))
    # pprint(chart_list, indent=4)

    chart.sort(key=lambda x: x.key)
    chart.sort(key=lambda x: x.count, reverse=True)

    # Determine how many gaps to leave beween lines.
    last_entry = chart[0]
    for entry in chart[1:]:

        if last_entry.count > entry.count + 1:
            last_entry.gap = last_entry.count - entry.count - 1

        last_entry = entry

    return chart


def print_chart(chart):
    for index, item in enumerate(chart):
        print("{:4}: ({:4}) - {}".format(index + 1, item.count, item.key))
        if item.count > 10 and item.count < 50:
            for line in range(item.gap):
                print("")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


def write_chart(fp, chart, title=None, summary=None, gaps=True):

    pos_justify = calculate_right_justify(len(chart))
    cnt_justify = calculate_right_justify(chart[0].count)

    if title is not None:
        write_title(fp, title)

    if summary is not None:
        write_summary(fp, summary)

    for index, item in enumerate(chart):

        pos = str(index + 1).rjust(pos_justify)
        cnt = str(item.count).rjust(cnt_justify)

        fp.write("{}: ({}) {} {}\n".format(pos, cnt, item.isowned, item.key))

        if item.count > 10 and item.count < 50:
            for line in range(item.gap):
                fp.write("\n")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


def write_title(fp, title):
    fp.write("{}\n".format(title))


def write_summary(fp, summary):
    fp.write(
        "{:8} {:13} {:13} {:13}\n".format(
            "Total Tracks", "Unique Artists", "Unique albums", "Unique Tracks"
        )
    )
    fp.write(
        "{:8} {:13} {:13} {:13}\n".format(
            summary.total_tracks,
            summary.unique_artists,
            summary.unique_albums,
            summary.unique_tracks,
        )
    )


def make_summary(tracks):
    """
    GIven a list of track, generates sumamry information for it.
    """
    unique_artists = {}
    unique_albums = {}
    unique_tracks = {}

    summary = SummaryEntry(0, 0, 0, 0)

    summary.total_tracks = len(tracks)

    for track in tracks:
        entry = TrackEntry(track[0], track[1], track[2], track[3])

        if entry.artist not in unique_artists:
            unique_artists[entry.artist] = 0
            summary.unique_artists += 1
        if entry.album not in unique_albums:
            unique_albums[entry.album] = 0
            summary.unique_albums += 1
        if entry.track not in unique_tracks:
            unique_tracks[entry.track] = 0
            summary.unique_tracks += 1

    return summary


# But also use partial function to supply key once, once we know it.
def get_key(key, artist, album, track):
    if key == "artist":
        return artist

    if key == "album":
        return " - ".join([album, artist])

    if key == "track":
        return "{} - {} ({})".format(track, artist, album)

    return None


def calculate_right_justify(len):
    if len > 1000:
        return 4
    # if len > 100:
    #     return 3
    # if len > 10:
    #     return 2

    return 3


if __name__ == "__main__":

    track1 = ["date1", "artist1", "album1", "track1"]
    track2 = ["date2", "artist2", "album2", "track2"]
    track3 = ["date2", "artist1", "album1", "track3"]
    track4 = ["date2", "artist1", "album1", "track4"]
    track5 = ["date2", "artist1", "album1", "track5"]
    tracks = [track1, track2, track3, track4, track5]

    print("Check artist list")
    chart = make_chart(tracks, "artist")
    print_chart(chart)

    print("Check album list")
    chart = make_chart(tracks, "album")
    print_chart(chart)

    print("Check track list")
    chart = make_chart(tracks, "track")
    print_chart(chart)

    # get_key_partial = partial(get_key, "artist")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1"

    # get_key_partial = partial(get_key, "album")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1 - album1"

    # get_key_partial = partial(get_key, "track")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1 - album1 - track1"

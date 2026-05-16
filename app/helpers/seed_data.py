from app.extensions import db
from app.models import Book, Comment, User, ShelfItem, Rating


STARTER_BOOKS = [
   {
       "title": 'The Midnight Library',
        "author": 'Matt Haig',
        "openlibrary_id": '/works/OL20965973W',
        "description": 'Between life and death there is a library, and within that library, the shelves go on forever. Every book provides a chance to try another life you could have lived. To see how things would be if you had made other choices . . . Would you have done anything different, if you had the chance to undo your regrets?”\r\n\r\nA dazzling novel about all the choices that go into a life well lived, from the internationally bestselling author of Reasons to Stay Alive and How To Stop Time.\r\n\r\nSomewhere out beyond the edge of the universe there is a library that contains an infinite number of books, each one the story of another reality. One tells the story of your life as it is, along with another book for the other life you could have lived if you had made a different choice at any point in your life. While we all wonder how our lives might have been, what if you had the chance to go to the library and see for yourself? Would any of these other lives truly be better?\r\n\r\nIn The Midnight Library, Matt Haig’s enchanting new novel, Nora Seed finds herself faced with this decision. Faced with the possibility of changing her life for a new one, following a different career, undoing old breakups, realizing her dreams of becoming a glaciologist; she must search within herself as she travels through the Midnight Library to decide what is truly fulfilling in life, and what makes it worth living in the first place.',
        "page_count": 318,
        "cover_url": 'https://covers.openlibrary.org/b/id/10313767-M.jpg',
        "rating": 4.0,
        "reads": 1320,
    },
    {
        "title": 'Project Hail Mary',
        "author": 'Andy Weir',
        "openlibrary_id": '/works/OL21745884W',
        "description": 'Ryland Grace is the sole survivor on a desperate, last-chance mission–and if he fails, humanity and the earth itself will perish. Except that right now, he doesn’t know that. He can’t even remember his own name, let alone the nature of his assignment or how to complete it. All he knows is that he’s been asleep for a very, very long time. And he’s just been awakened to find himself millions of miles from home, with nothing but two corpses for company.\r\n\r\nHis crewmates dead, his memories fuzzily returning, he realizes that an impossible task now confronts him. Alone on this tiny ship that’s been cobbled together by every government and space agency on the planet and hurled into the depths of space, it’s up to him to conquer an extinction-level threat to our species.\r\n\r\nAnd thanks to an unexpected ally, he just might have a chance.\r\n\r\nPart scientific mystery, part dazzling interstellar journey, *Project Hail Mary* is a tale of discovery, speculation, and survival to rival *The Martian*–while taking us to places it never dreamed of going.',
        "page_count": 424,
        "cover_url": 'https://covers.openlibrary.org/b/id/11200092-M.jpg',
        "rating": 5.0,
        "reads": 1680,
    },
    {
        "title": 'Tomorrow, and Tomorrow, and Tomorrow',
        "author": 'Gabrielle Zevin',
        "openlibrary_id": '/works/OL26004554W',
        "description": "On a bitter-cold day, in the December of his junior year at Harvard, Sam Masur exits a subway car and sees, amid the hordes of people waiting on the platform, Sadie Green. He calls her name. For a moment, she pretends she hasn't heard him, but then, she turns, and a game begins: a legendary collaboration that will launch them to stardom. These friends, intimates since childhood, borrow money, beg favors, and, before even graduating college, they have created their first blockbuster, Ichigo. Overnight, the world is theirs. Not even twenty-five years old, Sam and Sadie are brilliant, successful, and rich, but these qualities won't protect them from their own creative ambitions or the betrayals of their hearts.\r\n\r\nSpanning thirty years, from Cambridge, Massachusetts, to Venice Beach, California, and lands in between and far beyond, Gabrielle Zevin's Tomorrow, and Tomorrow, and Tomorrow is a dazzling and intricately imagined novel that examines the multifarious nature of identity, disability, failure, the redemptive possibilities in play, and above all, our need to connect: to be loved and to love. Yes, it is a love story, but it is not one you have read before.",
        "page_count": 415,
        "cover_url": 'https://covers.openlibrary.org/b/id/12859975-M.jpg',
        "rating": 4.0,
        "reads": 1540,
    },
    {
        "title": 'Lessons in Chemistry',
        "author": 'Bonnie Garmus',
        "openlibrary_id": '/works/OL25344431W',
        "description": 'Chemist Elizabeth Zott is not your average woman. In fact, Elizabeth Zott would be the first to point out that there is no such thing as an average woman. But it’s the early 1960s and her all-male team at Hastings Research Institute takes a very unscientific view of equality. Except for one: Calvin Evans; the lonely, brilliant, Nobel–prize nominated grudge-holder who falls in love with—of all things—her mind. True chemistry results.\r\n\r\nBut like science, life is unpredictable. Which is why a few years later Elizabeth Zott finds herself not only a single mother, but the reluctant star of America’s most beloved cooking show Supper at Six. Elizabeth’s unusual approach to cooking (“combine one tablespoon acetic acid with a pinch of sodium chloride”) proves revolutionary. But as her following grows, not everyone is happy. Because as it turns out, Elizabeth Zott isn’t just teaching women to cook. She’s daring them to change the status quo.',
        "page_count": 480,
        "cover_url": 'https://covers.openlibrary.org/b/id/12725772-M.jpg',
        "rating": 4.0,
        "reads": 1490,
    },
    {
        "title": 'Fourth Wing',
        "author": 'Rebecca Yarros',
        "openlibrary_id": '/works/OL29226517W',
        "description": "Twenty-year-old Violet Sorrengail was supposed to enter the Scribe Quadrant, living a quiet life among books and history. Now, the commanding general—also known as her tough-as-talons mother—has ordered Violet to join the hundreds of candidates striving to become the elite of Navarre: dragon riders.\r\n\r\nBut when you’re smaller than everyone else and your body is brittle, death is only a heartbeat away...because dragons don’t bond to “fragile” humans. They incinerate them.\r\n\r\nWith fewer dragons willing to bond than cadets, most would kill Violet to better their own chances of success. The rest would kill her just for being her mother’s daughter—like Xaden Riorson, the most powerful and ruthless wingleader in the Riders Quadrant.\r\n\r\nShe’ll need every edge her wits can give her just to see the next sunrise.\r\n\r\nYet, with every day that passes, the war outside grows more deadly, the kingdom's protective wards are failing, and the death toll continues to rise. Even worse, Violet begins to suspect leadership is hiding a terrible secret.\r\n\r\nFriends, enemies, lovers. Everyone at Basgiath War College has an agenda—because once you enter, there are only two ways out: graduate or die.",
        "page_count": 541,
        "cover_url": 'https://covers.openlibrary.org/b/id/14407898-M.jpg',
        "rating": 4.0,
        "reads": 2300,
    },
    {
        "title": 'Yellowface',
        "author": 'R. F. Kuang',
        "openlibrary_id": '/works/OL29050559W',
        "description": 'White lies. Dark humor. Deadly consequences… Bestselling sensation Juniper Song is not who she says she is, she didn’t write the book she claims she wrote, and she is most certainly not Asian American—in this chilling and hilariously cutting novel from R.F. Kuang, the #1 New York Times bestselling author of Babel.\r\n\r\nAuthors June Hayward and Athena Liu were supposed to be twin rising stars. But Athena’s a literary darling. June Hayward is literally nobody. Who wants stories about basic white girls, June thinks.\r\n\r\nSo when June witnesses Athena’s death in a freak accident, she acts on impulse: she steals Athena’s just-finished masterpiece, an experimental novel about the unsung contributions of Chinese laborers during World War I.\r\n\r\nSo what if June edits Athena’s novel and sends it to her agent as her own work? So what if she lets her new publisher rebrand her as Juniper Song—complete with an ambiguously ethnic author photo? Doesn’t this piece of history deserve to be told, whoever the teller? That’s what June claims, and the New York Times bestseller list seems to agree.\r\n\r\nBut June can’t get away from Athena’s shadow, and emerging evidence threatens to bring June’s (stolen) success down around her. As June races to protect her secret, she discovers exactly how far she will go to keep what she thinks she deserves.\r\n\r\nWith its totally immersive first-person voice, Yellowface grapples with questions of diversity, racism, and cultural appropriation, as well as the terrifying alienation of social media. R.F. Kuang’s novel is timely, razor-sharp, and eminently readable.',
        "page_count": 352,
        "cover_url": 'https://covers.openlibrary.org/b/id/13195421-M.jpg',
        "rating": 4.0,
        "reads": 1210,
    },
    {
        "title": 'Babel',
        "author": 'R. F. Kuang',
        "openlibrary_id": '/works/OL26443093W',
        "description": "From award-winning author R. F. Kuang comes Babel, a thematic response to The Secret History and a tonal retort to Jonathan Strange & Mr. Norrell that grapples with student revolutions, colonial resistance, and the use of language and translation as the dominating tool of the British empire.\r\n\r\nTraduttore, traditore: An act of translation is always an act of betrayal.\r\n\r\n1828. Robin Swift, orphaned by cholera in Canton, is brought to London by the mysterious Professor Lovell. There, he trains for years in Latin, Ancient Greek, and Chinese, all in preparation for the day he’ll enroll in Oxford University’s prestigious Royal Institute of Translation—also known as Babel.\r\n\r\nBabel is the world's center for translation and, more importantly, magic. Silver working—the art of manifesting the meaning lost in translation using enchanted silver bars—has made the British unparalleled in power, as its knowledge serves the Empire’s quest for colonization.\r\n\r\nFor Robin, Oxford is a utopia dedicated to the pursuit of knowledge. But knowledge obeys power, and as a Chinese boy raised in Britain, Robin realizes serving Babel means betraying his motherland. As his studies progress, Robin finds himself caught between Babel and the shadowy Hermes Society, an organization dedicated to stopping imperial expansion. When Britain pursues an unjust war with China over silver and opium, Robin must decide…\r\n\r\nCan powerful institutions be changed from within, or does revolution always require violence?",
        "page_count": 624,
        "cover_url": 'https://covers.openlibrary.org/b/id/12468631-M.jpg',
        "reads": 1420,
    },
    {
        "title": 'The Seven Husbands of Evelyn Hugo',
        "author": 'Taylor Jenkins Reid',
        "openlibrary_id": '/works/OL18203673W',
        "description": 'Aging and reclusive Hollywood movie icon Evelyn Hugo is finally ready to tell the truth about her glamorous and scandalous life. But when she chooses unknown magazine reporter Monique Grant for the job, no one is more astounded than Monique herself. Why her? Why now?\r\n\r\nMonique is not exactly on top of the world. Her husband has left her, and her professional life is going nowhere. Regardless of why Evelyn has selected her to write her biography, Monique is determined to use this opportunity to jumpstart her career.\r\n\r\nSummoned to Evelyn\'s luxurious apartment, Monique listens in fascination as the actress tells her story. From making her way to Los Angeles in the 1950s to her decision to leave show business in the \'80s, and, of course, the seven husbands along the way, Evelyn unspools a tale of ruthless ambition, unexpected friendship, and a great forbidden love. Monique begins to feel a very real connection to the legendary star, but as Evelyn\'s story near its conclusion, it becomes clear that her life intersects with Monique\'s own in tragic and irreversible ways.\r\n\r\nWritten with Reid\'s signature talent for creating "complex, likable characters" (Real Simple), this is a mesmerizing journey through the splendor of old Hollywood into the harsh realities of the present day as two women struggle with what it means—and what it costs—to face the truth',
        "page_count": 453,
        "cover_url": 'https://covers.openlibrary.org/b/id/8354226-M.jpg',
        "rating": 5.0,
        "reads": 2500,
    },
    {
        "title": 'Daisy Jones & The Six',
        "author": 'Taylor Jenkins Reid',
        "openlibrary_id": '/works/OL19922194W',
        "description": 'A gripping novel about the whirlwind rise of an iconic 1970s rock group and their beautiful lead singer, revealing the mystery behind their infamous break up.\r\n\r\nEveryone knows Daisy Jones & The Six, but nobody knows the real reason why they split at the absolute height of their popularity…until now.\r\n\r\nDaisy is a girl coming of age in L.A. in the late sixties, sneaking into clubs on the Sunset Strip, sleeping with rock stars, and dreaming of singing at the Whisky a Go-Go. The sex and drugs are thrilling, but it’s the rock and roll she loves most. By the time she’s twenty, her voice is getting noticed, and she has the kind of heedless beauty that makes people do crazy things.\r\n\r\nAnother band getting noticed is The Six, led by the brooding Billy Dunne. On the eve of their first tour, his girlfriend Camila finds out she’s pregnant, and with the pressure of impending fatherhood and fame, Billy goes a little wild on the road.\r\n\r\nDaisy and Billy cross paths when a producer realizes the key to supercharged success is to put the two together. What happens next will become the stuff of legend.',
        "page_count": 400,
        "cover_url": 'https://covers.openlibrary.org/b/id/8742674-M.jpg',
        "reads": 1380,
    },
    {
        "title": 'Where the Crawdads Sing',
        "author": 'Delia Owens',
        "openlibrary_id": '/works/OL18766691W',
        "description": 'For years, rumors of the “Marsh Girl” have haunted Barkley Cove, a quiet town on the North Carolina coast. So in late 1969, when handsome Chase Andrews is found dead, the locals immediately suspect Kya Clark, the so-called Marsh Girl. But Kya is not what they say. Sensitive and intelligent, she has survived for years alone in the marsh that she calls home, finding friends in the gulls and lessons in the sand. Then the time comes when she yearns to be touched and loved. When two young men from town become intrigued by her wild beauty, Kya opens herself to a new life–until the unthinkable happens.\r\n\r\nPerfect for fans of Barbara Kingsolver and Karen Russell, Where the Crawdads Sing is at once an exquisite ode to the natural world, a heartbreaking coming-of-age story, and a surprising tale of possible murder. Owens reminds us that we are forever shaped by the children we once were, and that we are all subject to the beautiful and violent secrets that nature keeps.',
        "page_count": 384,
        "cover_url": 'https://covers.openlibrary.org/b/id/8362947-M.jpg',
        "rating": 4.0,
        "reads": 1760,
    },
    {
        "title": 'It Ends With Us',
        "author": 'Colleen Hoover',
        "openlibrary_id": '/works/OL18020194W',
        "description": 'Lily hasn’t always had it easy, but that’s never stopped her from working hard for the life she wants. She’s come a long way from the small town where she grew up—she graduated from college, moved to Boston, and started her own business. And when she feels a spark with a gorgeous neurosurgeon named Ryle Kincaid, everything in Lily’s life seems too good to be true.\r\n\r\nRyle is assertive, stubborn, maybe even a little arrogant. He’s also sensitive, brilliant, and has a total soft spot for Lily. And the way he looks in scrubs certainly doesn’t hurt. Lily can’t get him out of her head. But Ryle’s complete aversion to relationships is disturbing. Even as Lily finds herself becoming the exception to his “no dating” rule, she can’t help but wonder what made him that way in the first place.\r\n\r\nAs questions about her new relationship overwhelm her, so do thoughts of Atlas Corrigan—her first love and a link to the past she left behind. He was her kindred spirit, her protector. When Atlas suddenly reappears, everything Lily has built with Ryle is threatened.\r\n\r\nWith this bold and deeply personal novel, It Ends With Us is a heart-wrenching story and an unforgettable tale of love that comes at the ultimate price.',
        "page_count": 412,
        "cover_url": 'https://covers.openlibrary.org/b/id/10473609-M.jpg',
        "rating": 4.0,
        "reads": 2100,
    },
    {
        "title": 'Verity',
        "author": 'Colleen Hoover',
        "openlibrary_id": '/works/OL20068530W',
        "description": "Lowen Ashleigh is a struggling writer on the brink of financial ruin when she accepts the job offer of a lifetime. Jeremy Crawford, husband of bestselling author Verity Crawford, has hired Lowen to complete the remaining books in a successful series his injured wife is unable to finish.\r\n \r\nLowen arrives at the Crawford home, ready to sort through years of Verity’s notes and outlines, hoping to find enough material to get her started. What Lowen doesn’t expect to uncover in the chaotic office is an unfinished autobiography Verity never intended for anyone to read. Page after page of bone-chilling admissions, including Verity's recollection of the night her family was forever altered.\r\n \r\nLowen decides to keep the manuscript hidden from Jeremy, knowing its contents could devastate the already grieving father. But as Lowen’s feelings for Jeremy begin to intensify, she recognizes all the ways she could benefit if he were to read his wife’s words. After all, no matter how devoted Jeremy is to his injured wife, a truth this horrifying would make it impossible for him to continue loving her.",
        "page_count": 269,
        "cover_url": 'https://covers.openlibrary.org/b/id/8747160-M.jpg',
        "reads": 1900,
    },
    {
        "title": 'Normal People',
        "author": 'Sally Rooney',
        "openlibrary_id": '/works/OL20150260W',
        "description": 'At school Connell and Marianne pretend not to know each other. He’s popular and well-adjusted, star of the school soccer team while she is lonely, proud, and intensely private. But when Connell comes to pick his mother up from her housekeeping job at Marianne’s house, a strange and indelible connection grows between the two teenagers - one they are determined to conceal.\r\n\r\nA year later, they’re both studying at Trinity College in Dublin. Marianne has found her feet in a new social world while Connell hangs at the sidelines, shy and uncertain. Throughout their years in college, Marianne and Connell circle one another, straying toward other people and possibilities but always magnetically, irresistibly drawn back together. Then, as she veers into self-destruction and he begins to search for meaning elsewhere, each must confront how far they are willing to go to save the other.\r\n\r\nSally Rooney brings her brilliant psychological acuity and perfectly spare prose to a story that explores the subtleties of class, the electricity of first love, and the complex entanglements of family and friendship.',
        "page_count": 320,
        "cover_url": 'https://covers.openlibrary.org/b/id/8794265-M.jpg',
        "reads": 980,
    },
    {
        "title": 'Beautiful World, Where Are You',
        "author": 'Sally Rooney',
        "openlibrary_id": '/works/OL24151602W',
        "description": 'Three friends and a hanger-on gradually coalesce into two couples.',
        "page_count": 352,
        "cover_url": 'https://covers.openlibrary.org/b/id/10550746-M.jpg',
        "reads": 860,
    },
    {
        "title": 'Before the Coffee Gets Cold',
        "author": 'Toshikazu Kawaguchi',
        "openlibrary_id": '/works/OL20832477W',
        "description": 'If you could go back in time, who would you want to meet?\r\n\r\nIn a small back alley of Tokyo, there is a café that has been serving carefully brewed coffee for more than one hundred years. Local legend says that this shop offers something else besides coffee—the chance to travel back in time.\r\n\r\nOver the course of one summer, four customers visit the café in the hopes of making that journey. But time travel isn’t so simple, and there are rules that must be followed. Most important, the trip can last only as long as it takes for the coffee to get cold.\r\n\r\nHeartwarming, wistful, mysterious and delightfully quirky, Toshikazu Kawaguchi’s internationally bestselling novel explores the age-old question: What would you change if you could travel back in time?',
        "page_count": 239,
        "cover_url": 'https://covers.openlibrary.org/b/id/10138333-M.jpg',
        "reads": 1120,
    },
    {
        "title": 'The Invisible Life of Addie LaRue',
        "author": 'V. E. Schwab',
        "openlibrary_id": '/works/OL20796936W',
        "description": 'France, 1714: in a moment of desperation, a young woman makes a Faustian bargain to live forever and is cursed to be forgotten by everyone she meets.\r\n\r\nThus begins the extraordinary life of Addie LaRue, and a dazzling adventure that will play out across centuries and continents, across history and art, as a young woman learns how far she will go to leave her mark on the world.\r\n\r\nBut everything changes when, after nearly 300 years, Addie stumbles across a young man in a hidden bookstore and he remembers her name.',
        "page_count": 655,
        "cover_url": 'https://covers.openlibrary.org/b/id/10092261-M.jpg',
        "reads": 1600,
    },
    {
        "title": 'Circe',
        "author": 'Madeline Miller',
        "openlibrary_id": '/works/OL18012166W',
        "description": "In the house of Helios, god of the sun and mightiest of the Titans, a daughter is born. But Circe is a strange child--not powerful, like her father, nor viciously alluring like her mother. Turning to the world of mortals for companionship, she discovers that she does possess power--the power of witchcraft, which can transform rivals into monsters and menace the gods themselves.\r\n\r\nThreatened, Zeus banishes her to a deserted island, where she hones her occult craft, tames wild beasts and crosses paths with many of the most famous figures in all of mythology, including the Minotaur, Daedalus and his doomed son Icarus, the murderous Medea, and, of course, wily Odysseus.\r\n\r\nBut there is danger, too, for a woman who stands alone, and Circe unwittingly draws the wrath of both men and gods, ultimately finding herself pitted against one of the most terrifying and vengeful of the Olympians. To protect what she loves most, Circe must summon all her strength and choose, once and for all, whether she belongs with the gods she is born from, or the mortals she has come to love.\r\n\r\nWith unforgettably vivid characters, mesmerizing language and page-turning suspense, Circe is a triumph of storytelling, an intoxicating epic of family rivalry, palace intrigue, love and loss, as well as a celebration of indomitable female strength in a man's world.\r\n([source][1])\r\n\r\n\r\n  [1]: http://madelinemiller.com/circe/",
        "page_count": 488,
        "cover_url": 'https://covers.openlibrary.org/b/id/8739376-M.jpg',
        "reads": 1700,
    },
    {
        "title": 'The Song of Achilles',
        "author": 'Madeline Miller',
        "openlibrary_id": '/works/OL16509148W',
        "description": 'This is the story of the seige of Troy from the perspective of Achilles best-friend Patroclus.  Although Patroclus is outcast from his home for disappointing his father he manages to be the only mortal who can keep up with the half-God Archilles.  Even though many will know the facts behind the story the telling is fresh and engaging.',
        "page_count": 352,
        "cover_url": 'https://covers.openlibrary.org/b/id/7098465-M.jpg',
        "rating": 5.0,
        "reads": 2200,
    },
    {
        "title": 'The House in the Cerulean Sea',
        "author": 'T. J. Klune',
        "openlibrary_id": '/works/OL20656224W',
        "description": 'Linus is an uptight caseworker with a heart of gold working for the department in charge of magical youth. When he goes to investigate an orphanage on an island with supposedly dangerous children and an enigmatic leader Arthur, he’s expecting the worst. But it turns out he might be falling in love with Arthur and his charges.',
        "page_count": 416,
        "cover_url": 'https://covers.openlibrary.org/b/id/9312772-M.jpg',
        "reads": 1480,
    },
    {
        "title": 'A Court of Thorns and Roses',
        "author": 'Sarah J. Maas',
        "openlibrary_id": '/works/OL17352669W',
        "description": "When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.\r\n\r\nAt least, he's not a beast all the time.\r\n\r\nAs she adapts to her new home, her feelings for the faerie, Tamlin, transform from icy hostility into a fiery passion that burns through every lie she's been told about the beautiful, dangerous world of the Fae. But something is not right in the faerie lands. An ancient, wicked shadow is growing, and Feyre must find a way to stop it, or doom Tamlin-and his world-forever.",
        "page_count": 456,
        "cover_url": 'https://covers.openlibrary.org/b/id/8738585-M.jpg',
        "rating": 4.0,
        "reads": 2400,
    },
]

STARTER_USERS = [
    {
        "name": "Reader1",
        "username": "reader1",
        "email": "reader1@example.com",
        "password": "password123",
    },
    {
        "name": "Tom Harris",
        "username": "tom",
        "email": "tom@example.com",
        "password": "password123",
        "bio": "Sci-fi reader and space enthusiast.",
        "avatar": "../static/images/seed_avatars/tom.jpg",
    },
    {
        "name": "Mia Chen",
        "username": "mia",
        "email": "mia@example.com",
        "password": "password123",
        "bio": "Loves literary fiction and indie games.",
        "avatar": "../static/images/seed_avatars/mia.jpg",
    },
    {
        "name": "Alice",
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "bio": "You can find me curled up with a book!",
        "avatar": "../static/images/seed_avatars/alice.jpg",
    },
    {
        "name": "Bookdragon",
        "username": "bookdragon",
        "email": "bookdragon@example.com",
        "password": "password123",
    },
    {
        "name": "Sam",
        "username": "sam",
        "email": "sam@example.com",
        "password": "password123",
    },
    {
        "name": "Emma Clarke",
        "username": "emma",
        "email": "emma@example.com",
        "password": "password123",
        "bio": "Always reading emotional dramas.",
        "avatar": "../static/images/seed_avatars/emma.jpg",
    },
    {
        "name": "Lily E",
        "username": "lily",
        "email": "lily@example.com",
        "password": "password123",
        "bio": "Loves any romance novel.",
        "avatar": "../static/images/seed_avatars/lily.jpg",
    },
    {
        "name": "Alex",
        "username": "alex",
        "email": "alex@example.com",
        "password": "password123",
    },
    {
        "name": "Yana",
        "username": "fantasyfan",
        "email": "yana@example.com",
        "password": "password123",
        "bio": "I love fantasy.",
        "avatar": "../static/images/seed_avatars/fantasyfan.jpg",
    },
]

STARTER_SHELVES = [
    {
        "username": "reader1",
        "status": "Read",
        "books": [
            "The Midnight Library",
            "Tomorrow, and Tomorrow, and Tomorrow",
            "Normal People",
            "Babel",
            "Yellowface",
        ],
    },
    {
        "username": "tom",
        "status": "Read",
        "books": [
            "Project Hail Mary",
            "The Midnight Library",
            "Tomorrow, and Tomorrow, and Tomorrow",
        ],
    },
    {
        "username": "tom",
        "status": "Currently Reading",
        "books": ["Circe"],
    },
    {
        "username": "tom",
        "status": "To Be Read",
        "books": [
            "Beautiful World, Where Are You",
            "The House in the Cerulean Sea",

        ],
    },
    {
        "username": "tom",
        "status": "Did Not Finish",
        "books": ["Where the Crawdads Sing"],
    },
    {
        "username": "alice",
        "status": "Read",
        "books": [
            "Fourth Wing",
            "The Seven Husbands of Evelyn Hugo",
            "Daisy Jones & The Six",
            "Normal People",
            "The Invisible Life of Addie LaRue",
            "A Court of Thorns and Roses",
            "Verity",
            "Lessons in Chemistry",
            "It Ends With Us",
        ],
    },
    {
        "username": "alice",
        "status": "Currently Reading",
        "books": ["Babel"],
    },
    {
        "username": "alice",
        "status": "To Be Read",
        "books": [
            "Where the Crawdads Sing",
            "Before the Coffee Gets Cold",
        ],
    },
    {
        "username": "alice",
        "status": "Did Not Finish",
        "books": ["Beautiful World, Where Are You"],
    },
    {
        "username": "fantasyfan",
        "status": "Read",
        "books": [
            "A Court of Thorns and Roses",
            "Fourth Wing",
            "Circe",
            "The Midnight Library",
            "The Song of Achilles",
            "The House in the Cerulean Sea",
        ],
    },
    {
        "username": "fantasyfan",
        "status": "Currently Reading",
        "books": [
            "The Seven Husbands of Evelyn Hugo",
            "Daisy Jones & The Six",
            "Verity",
        ],
    },
    {
        "username": "fantasyfan",
        "status": "To Be Read",
        "books": [
            "Lessons in Chemistry",
        ],
    },
    {
        "username": "mia",
        "status": "Read",
        "books": [
            "Normal People",
            "Tomorrow, and Tomorrow, and Tomorrow",
        ],
    },
    {
        "username": "alex",
        "status": "Read",
        "books": [
            "The Song of Achilles",
            "Circe",
        ],
    },
    {
        "username": "emma",
        "status": "Read",
        "books": [
            "The Seven Husbands of Evelyn Hugo",
            "Verity",
            "Where the Crawdads Sing",
            "Normal People",
            "The Invisible Life of Addie LaRue",
        ],
    },
    {
        "username": "emma",
        "status": "Currently Reading",
        "books": [
            "The Song of Achilles",
            "Circe",
        ],
    },
    {
        "username": "sam",
        "status": "Read",
        "books": [
            "Yellowface",
            "Circe",
        ],
    },
    {
        "username": "lily",
        "status": "Read",
        "books": [
            "A Court of Thorns and Roses",
            "Lessons in Chemistry",
            "Fourth Wing",
            "Normal People",
            "Circe",
            "The Midnight Library",
            "The Song of Achilles",
            "The House in the Cerulean Sea",
            "Beautiful World, Where Are You",
            "Where the Crawdads Sing",
        ],
    },
    {
        "username": "lily",
        "status": "Currently Reading",
        "books": [
            "Verity",
            "Project Hail Mary",
        ],
    },
]

STARTER_FAVOURITES = [
    {
        "username": "tom",
        "books": [
            "Project Hail Mary",
            "The Song of Achilles",
        ]
    },
    {
        "username": "alice",
        "books": [
            "The Seven Husbands of Evelyn Hugo",
            "Normal People",
            "The Invisible Life of Addie LaRue",
            "A Court of Thorns and Roses",
            "Verity",
            "Fourth Wing",
        ]
    },
    {
        "username": "mia",
        "books": [
            "Normal People",
            "Tomorrow, and Tomorrow, and Tomorrow",
        ]
    },
    {
        "username": "fantasyfan",
        "books": [
            "A Court of Thorns and Roses",
            "Fourth Wing",
            "The House in the Cerulean Sea",
        ]
    },
    {
        "username": "bookdragon",
        "books": [
            "A Court of Thorns and Roses",
            "Fourth Wing",
            "Verity",
            "Where the Crawdads Sing",
        ]
    },
    {
        "username": "emma",
        "books": [
            "The Seven Husbands of Evelyn Hugo",
            "Verity",
            "Where the Crawdads Sing",
            "Normal People",
            "The Invisible Life of Addie LaRue",
        ]
    },
]

STARTER_FOLLOWS = [
    ("reader1", "tom"),
    ("reader1", "bookdragon"),
    ("tom", "mia"),
    ("tom", "alice"),
    ("tom", "alex"),
    ("tom", "reader1"),
    ("tom", "sam"),
    ("alice", "tom"),
    ("alice", "mia"),
    ("alice", "fantasyfan"),
    ("alice", "lily"),  
    ("mia", "emma"),
    ("mia", "alice"),
    ("emma", "tom"),
    ("emma", "alice"),
    ("emma", "mia"),
    ("emma", "lily"),
    ("fantasyfan", "lily"),
    ("fantasyfan", "alice"),
    ("fantasyfan", "tom"),
    ("fantasyfan", "mia"),
    ("fantasyfan", "bookdragon"),
    ("fantasyfan", "emma"),
    ("alex", "tom"),
    ("alex", "alice"),
    ("alex", "fantasyfan"),
    ("alex", "sam"),
    ("sam", "tom"),
    ("sam", "alex"),
]

STARTER_COMMENTS = [
    {
        "book_title": "The Midnight Library",
        "username": "reader1",
        "stars": 4,
        "text": "A thoughtful story about regret, choices, and learning what really matters in life.",
    },
    {
        "book_title": "Project Hail Mary",
        "username": "tom",
        "stars": 5,
        "text": "Very fun sci-fi with clever problem solving and a surprisingly emotional story.",
    },
    {
        "book_title": "Tomorrow, and Tomorrow, and Tomorrow",
        "username": "mia",
        "stars": 4,
        "text": "I liked how it connects friendship, creativity, games, and growing up.",
    },
    {
        "book_title": "Lessons in Chemistry",
        "username": "alice",
        "stars": 4,
        "text": "Easy to read and inspiring, with a strong main character and a lot of humour.",
    },
    {
        "book_title": "Fourth Wing",
        "username": "bookdragon",
        "stars": 5,
        "text": "Fast-paced fantasy with dragons, action, romance, and lots of tension.",
    },
    {
        "book_title": "Yellowface",
        "username": "sam",
        "stars": 4,
        "text": "Sharp, uncomfortable, and interesting. It gives you a lot to think about.",
    },
    {
        "book_title": "The Seven Husbands of Evelyn Hugo",
        "username": "emma",
        "stars": 5,
        "text": "Emotional and dramatic. The story kept me interested from beginning to end.",
    },
    {
        "book_title": "Where the Crawdads Sing",
        "username": "lily",
        "stars": 4,
        "text": "Beautiful setting and a mysterious story. Some parts are slow, but still enjoyable.",
    },
    {
        "book_title": "The Song of Achilles",
        "username": "alex",
        "stars": 5,
        "text": "A beautiful and heartbreaking retelling. The writing feels simple but powerful.",
    },
    {
        "book_title": "A Court of Thorns and Roses",
        "username": "fantasyfan",
        "stars": 4,
        "text": "A good start to the series, especially if you like fantasy romance and fae worlds.",
    },
    {
        "book_title": "It Ends With Us",
        "username": "alice",
        "stars": 4,
        "text": "A heartbreaking story about breaking the cycle.",
    },
]


def seed_books_if_empty():
    if Book.query.first():
        return

    created_books = {}

    for book_data in STARTER_BOOKS:
        book = Book(
            title=book_data["title"],
            author=book_data["author"],
            description=book_data.get("description"),
            page_count=book_data.get("page_count"),
            cover_url=book_data.get("cover_url"),
            openlibrary_id=book_data.get("openlibrary_id"),
            rating=book_data.get("rating", 0),
            reads=book_data.get("reads", 0),
        )

        db.session.add(book)
        created_books[book.title] = book

    db.session.commit()

    created_users = {}

    for user_data in STARTER_USERS:
        user = User(
            name=user_data["name"],
            username=user_data["username"],
            email=user_data["email"],
            bio=user_data.get("bio", ""),
            avatar=user_data.get("avatar"),
        )

        user.set_password(user_data["password"])

        db.session.add(user)
        created_users[user.username] = user
    
    db.session.commit()

    shelf_items = []

    for shelf_data in STARTER_SHELVES:
        user = created_users.get(shelf_data["username"])

        if not user:
            continue

        for title in shelf_data["books"]:
            book = created_books.get(title)

            if not book:
                continue

            shelf_items.append(
                ShelfItem(
                    user_id=user.id,
                    book_id=book.id,
                    status=shelf_data["status"],
                )
            )

    db.session.add_all(shelf_items)
    db.session.commit()

    for favorite_data in STARTER_FAVOURITES:
        user = created_users.get(favorite_data["username"])

        if not user:
            continue

        for title in favorite_data["books"]:
            book = created_books.get(title)

            if book:
                user.favorite_books.append(book)

    db.session.commit()

    for follower_username, followed_username in STARTER_FOLLOWS:
        follower = created_users.get(follower_username)
        followed = created_users.get(followed_username)

        if follower and followed:
            follower.follow(followed)

    db.session.commit()    

    comments = []
    ratings = []

    for comment_data in STARTER_COMMENTS:
        book = created_books.get(comment_data["book_title"])
        user = created_users.get(comment_data["username"])

        if book:
            comments.append(
                Comment(
                    username=user.username,
                    user_id=user.id,
                    book_id=book.id,
                    stars=comment_data["stars"],
                    text=comment_data["text"],
                )
            )

            ratings.append(
                Rating(
                    username=user.username,
                    user_id=user.id,
                    book_id=book.id,
                    stars=comment_data["stars"],
                )
            )

    db.session.add_all(comments)
    db.session.add_all(ratings)
    db.session.commit()
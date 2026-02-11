import random
from itertools import cycle

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group

from accounts.models import AgentProfile
from Properties.models import Properties  # change to "properties.models" if your app folder is lowercase


class Command(BaseCommand):
    help = "Seed properties and distribute them across all Agent users"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # 1) Get Agent group
        agent_group = Group.objects.filter(name="Agent").first()
        if not agent_group:
            self.stdout.write(self.style.ERROR("Group 'Agent' not found. Create it first."))
            return

        # 2) Get all users in Agent group
        agent_users = list(User.objects.filter(groups=agent_group))
        if not agent_users:
            self.stdout.write(self.style.ERROR("No users found in 'Agent' group."))
            return

        # 3) Ensure each agent has an AgentProfile
        for user in agent_users:
            AgentProfile.objects.get_or_create(user=user)

        # 4) Distribute evenly across agents
        agent_cycle = cycle(agent_users)

        # 5) Locations (your list)
        locations = {
            "Lekki": ["Admiralty Way", "Freedom Way", "Chevron Drive"],
            "Ikoyi": ["Bourdillon Road", "Kingsway Road", "Awolowo Road"],
            "Ajah": ["Sangotedo Road", "Badore Road", "Addo Road"],
            "Ikeja": ["Allen Avenue", "Opebi Road", "Toyosi Street"],
            "Abuja": ["Gwarinpa Road", "Wuse Zone 2", "Maitama Crescent"],
            "Port Harcourt": ["GRA Phase 2", "Ada George Road", "Peter Odili Road"],
        }

        property_titles = [
            "Luxury Detached Duplex",
            "Modern 3 Bedroom Apartment",
            "Executive Bungalow",
            "Serviced Mini Flat",
            "Contemporary Terrace House",
            "Smart Home Apartment",
            "Penthouse Suite",
            "Spacious Family Home",
            "Luxury Studio Apartment",
            "Newly Built 2 Bedroom Flat",
        ]

        def price_by_location(city: str) -> int:
            """
            Keep within max_digits=10, decimal_places=2 (max 99,999,999.99)
            """
            if city in ["Ikoyi", "Abuja"]:
                return random.randint(40_000_000, 95_000_000)
            if city == "Lekki":
                return random.randint(25_000_000, 70_000_000)
            if city == "Ajah":
                return random.randint(10_000_000, 35_000_000)
            if city == "Port Harcourt":
                return random.randint(12_000_000, 55_000_000)
            # Ikeja (mixed)
            return random.randint(8_000_000, 60_000_000)

        created = 0

        # 6) Create 50 properties
        for i in range(1, 51):
            agent_user = next(agent_cycle)

            city = random.choice(list(locations.keys()))
            street = random.choice(locations[city])

            title = random.choice(property_titles)
            address = f"{random.randint(1, 80)} {street}, {city}"

            prop = Properties.objects.create(
                title=f"{title} in {city}",
                price=price_by_location(city),
                address=address,
                agent=agent_user,
                bedrooms=random.randint(1, 5),
                living_rooms=random.randint(1, 2),
                Sqm=random.randint(80, 450),
                bathrooms=random.randint(1, 4),
                property_type=random.choice(["Rent", "Sale"]),
                description="Clean and modern property in a secured estate with good road network and steady utilities.",
                is_featured=(i % 10 == 0),  # every 10th property featured
            )

            # Always attach a dummy image so templates don't crash
            prop.image.save(
                f"property_{i}.jpg",
                ContentFile(b"dummy image content"),
                save=True
            )

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created} properties distributed across {len(agent_users)} agents."
        ))

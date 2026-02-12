import random
from itertools import cycle
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File

from accounts.models import AgentProfile
from Properties.models import Properties, PropertyImage


class Command(BaseCommand):
    help = "Seed 20 properties with main images (seed_image) and extra images (seed_image2)"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # 1️⃣ Get Agent group
        agent_group = Group.objects.filter(name="Agent").first()
        if not agent_group:
            self.stdout.write(self.style.ERROR("Group 'Agent' not found."))
            return

        agent_users = list(User.objects.filter(groups=agent_group))
        if not agent_users:
            self.stdout.write(self.style.ERROR("No users found in 'Agent' group."))
            return

        # Ensure each has profile
        for user in agent_users:
            AgentProfile.objects.get_or_create(user=user)

        agent_cycle = cycle(agent_users)

        # 📁 Base project directory
        BASE_DIR = Path(__file__).resolve().parents[3]
        self.stdout.write(self.style.WARNING(f"BASE_DIR = {BASE_DIR}"))


        main_seed_dir = BASE_DIR / "seed_image"
        extra_seed_dir = BASE_DIR / "seed_image2"

        if not main_seed_dir.exists():
            self.stdout.write(self.style.ERROR("seed_image folder not found."))
            return

        if not extra_seed_dir.exists():
            self.stdout.write(self.style.ERROR("seed_image2 folder not found."))
            return

        allowed_ext = {".jpg", ".jpeg", ".png", ".webp"}

        main_images = [
            p for p in main_seed_dir.iterdir()
            if p.is_file() and p.suffix.lower() in allowed_ext
        ]

        extra_images = [
            p for p in extra_seed_dir.iterdir()
            if p.is_file() and p.suffix.lower() in allowed_ext
        ]

        if not main_images:
            self.stdout.write(self.style.ERROR("No images found in seed_image/"))
            return

        if not extra_images:
            self.stdout.write(self.style.ERROR("No images found in seed_image2/"))
            return

        # 10 STATES
        locations = {
            "Lagos": ["Lekki", "Ikoyi", "Ajah", "Ikeja"],
            "FCT Abuja": ["Wuse", "Maitama", "Gwarinpa"],
            "Rivers": ["Port Harcourt GRA", "Ada George"],
            "Ogun": ["Abeokuta", "Mowe"],
            "Oyo": ["Ibadan", "Bodija"],
            "Enugu": ["New Haven", "Independence Layout"],
            "Anambra": ["Awka", "Onitsha"],
            "Akwa Ibom": ["Uyo"],
            "Kano": ["Sabon Gari"],
            "Kaduna": ["Barnawa"],
        }

        titles = [
            "Luxury Detached Duplex",
            "Modern Apartment",
            "Executive Bungalow",
            "Serviced Flat",
            "Penthouse Suite",
            "Family Home",
        ]

        def price_by_state(state):
            if state in ["Lagos", "FCT Abuja"]:
                return random.randint(30_000_000, 200_000_000)
            if state == "Rivers":
                return random.randint(20_000_000, 150_000_000)
            return random.randint(8_000_000, 90_000_000)

        created = 0

        for i in range(1, 21):  # ✅ 20 properties
            agent_user = next(agent_cycle)

            state = random.choice(list(locations.keys()))
            area = random.choice(locations[state])

            prop = Properties.objects.create(
                title=f"{random.choice(titles)} in {area}",
                price=price_by_state(state),
                address=f"{random.randint(1, 100)} Estate Road, {area}",
                state=state,
                agent=agent_user,
                bedrooms=random.randint(1, 6),
                living_rooms=random.randint(1, 3),
                Sqm=random.randint(80, 600),
                bathrooms=random.randint(1, 5),
                property_type=random.choice(["Rent", "Sale"]),
                description="Beautiful property in a secure and serene environment.",
                is_featured=(i % 5 == 0),
            )

            # ✅ MAIN IMAGE from seed_image/
            main_path = random.choice(main_images)
            with open(main_path, "rb") as f:
                prop.image.save(
                    f"main_{prop.id}{main_path.suffix.lower()}",
                    File(f),
                    save=True
                )

            # ✅ EXTRA IMAGES from seed_image2/
            extra_count = random.randint(2, 5)
            selected_extras = random.sample(
                extra_images,
                k=min(extra_count, len(extra_images))
            )

            for idx, img_path in enumerate(selected_extras, start=1):
                extra = PropertyImage(property=prop)
                with open(img_path, "rb") as f:
                    extra.image.save(
                        f"extra_{prop.id}_{idx}{img_path.suffix.lower()}",
                        File(f),
                        save=True
                    )

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully created {created} properties with main and extra images."
        ))

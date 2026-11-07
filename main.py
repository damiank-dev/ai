import discord
from discord import app_commands
from discord.ext import commands

# Konfiguracja bota z domyślnymi intencji
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# Definicja okienka (Modal) z polem tekstowym dla komendy /script
class PromptModal(discord.ui.Modal, title="Generator Profesjonalnych Promptów"):
  user_input = discord.ui.TextInput(
      label="Opisz swój pomysł lub zadanie",
      style=discord.TextStyle.paragraph,
      placeholder=(
          "Np. Chcę napisać skrypt w Luau do Roblox Studio na system"
          " sklepiku..."
      ),
      required=True,
      max_length=1000,
  )

  async def on_submit(self, interaction: discord.Interaction):
    # Informacja o przetwarzaniu (przydatne, gdyby proces trwał dłużej)
    await interaction.response.defer(thinking=True)

    raw_text = self.user_input.value

    # Struktura profesjonalnego promptu generowanego na podstawie wpisu użytkownika
    refined_prompt = (
        "### ROLA I CEL\n"
        "Jesteś wybitnym ekspertem i programistą. Twoim zadaniem jest dostarczenie "
        "optymalnego, czystego i w pełni przemyślanego rozwiązania na podstawie "
        "poniższych wytycznych.\n\n"
        "### WYTYCZNE UŻYTKOWNIKA\n"
        f"{raw_text}\n\n"
        "### WYMAGANE OUTPUTY\n"
        "- Napisz kod zgodnie z najlepszymi praktykami.\n"
        "- Unikaj zbędnych komentarzy, skup się na optymalizacji.\n"
        "- Zapewnij obsługę błędów."
    )

    # Wysłanie wyniku w formie estetycznego Embeda
    embed = discord.Embed(
        title="✨ Wygenerowany Prompt",
        description=f"Oto zoptymalizowany prompt dla:\n> *{raw_text}*",
        color=0x5865F2,
    )
    embed.add_field(name="Wynik:", value=f"```markdown\n{refined_prompt}\n```")
    embed.set_footer(text=f"Wygenerowano dla {interaction.user.name}")

    await interaction.followup.send(embed=embed)


@bot.event
async def on_ready():
  print(
      f"Zalogowano jako {bot.user} (ID: {bot.user.id})\nSynchronizacja komend..."
  )
  try:
    synced = await bot.tree.sync()
    print(f"Zsynchronizowano {len(synced)} komend slash.")
  except Exception as e:
    print(e)


# Rejestracja komendy /script
@bot.tree.command(
    name="script", description="Otwiera generator profesjonalnych promptów."
)
async def script_command(interaction: discord.Interaction):
  await interaction.response.send_modal(PromptModal())


# Uruchomienie bota (wklej tutaj token swojego bota z Discord Developer Portal)
bot.run("TWÓJ_TOKEN_DISCORD_BOTA")

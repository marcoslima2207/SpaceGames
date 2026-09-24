import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { DatePipe, DecimalPipe, UpperCasePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AccountSummary, Game, GamesService } from './games.service';

@Component({
  selector: 'sg-account-page',
  standalone: true,
  imports: [RouterLink, UpperCasePipe, DatePipe, DecimalPipe],
  templateUrl: './account-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AccountPageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly gamesService = inject(GamesService);
  readonly mode = this.route.snapshot.data['mode'] as string;
  readonly games = signal<Game[]>([]);
  readonly account = signal<AccountSummary | undefined>(undefined);
  readonly authenticated = signal(Boolean(localStorage.getItem('spacegames_access')));
  readonly title = this.mode === 'biblioteca' ? 'Minha biblioteca' : this.mode === 'favoritos' ? 'Meus favoritos' : this.mode === 'perfil' ? 'Meu perfil' : 'Seu carrinho';
  readonly description = this.mode === 'biblioteca' ? 'Tudo o que você já conquistou, em um só lugar.' : this.mode === 'favoritos' ? 'Os jogos que você quer acompanhar de perto.' : this.mode === 'perfil' ? 'Sua identidade e seu histórico no SpaceGames.' : 'Sua próxima sessão começa aqui.';

  ngOnInit(): void {
    if (!this.authenticated()) return;
    this.loadAccount();
  }

  removeFromCart(itemId: number): void {
    this.gamesService.removeFromCart(itemId).subscribe(() => this.loadAccount());
  }

  checkout(): void {
    this.gamesService.checkout().subscribe(() => this.loadAccount());
  }

  private loadAccount(): void {
    this.gamesService.getAccountSummary().subscribe({
      next: (account) => {
        this.account.set(account);
        this.games.set(this.mode === 'biblioteca' ? account.biblioteca : this.mode === 'favoritos' ? account.favoritos : this.mode === 'perfil' ? [] : account.carrinho.map((item) => item.jogo));
      },
      error: () => this.authenticated.set(false)
    });
  }
  imageUrl(game: Game): string { return game.imagem_url_publica || game.imagem || 'https://placehold.co/900x560/120b20/d0b2ff?text=SPACEGAMES'; }
}
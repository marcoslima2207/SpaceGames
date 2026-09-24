import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Game, GamesService, Review } from './games.service';

@Component({
  selector: 'sg-game-detail',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './game-detail.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameDetailComponent implements OnInit {
  private readonly gamesService = inject(GamesService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly game = signal<Game | undefined>(undefined);
  readonly loading = signal(true);
  readonly message = signal('');
  readonly reviews = signal<Review[]>([]);
  reviewNote = 5;
  reviewComment = '';

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gamesService.getGames().subscribe((games) => { this.game.set(games.find((item) => item.id === id)); this.loading.set(false); });
    this.gamesService.getReviews(id).subscribe((reviews) => this.reviews.set(reviews));
  }
  imageUrl(game: Game): string { return game.imagem_url_publica || game.imagem || 'https://placehold.co/900x560/120b20/d0b2ff?text=SPACEGAMES'; }
  formatPrice(game: Game): string { return game.gratuito ? 'GRÁTIS' : Number(game.preco).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
  toggleFavorite(): void { this.runAction((id) => this.gamesService.toggleFavorite(id), 'Favorito atualizado.'); }
  addToCart(): void { this.runAction((id) => this.gamesService.addToCart(id), 'Jogo adicionado ao carrinho.'); }
  addFreeGame(): void { this.runAction((id) => this.gamesService.addFreeGame(id), 'Jogo adicionado à biblioteca.'); }
  saveReview(): void {
    const current = this.game();
    if (!current) return;
    if (!localStorage.getItem('spacegames_access')) { this.router.navigateByUrl('/login'); return; }
    this.gamesService.saveReview(current.id, this.reviewNote, this.reviewComment).subscribe({
      next: (review) => { this.reviews.update((items) => [review, ...items.filter((item) => item.usuario_nome !== review.usuario_nome)]); this.message.set('Avaliação publicada.'); },
      error: (response: { error?: { detail?: string } }) => this.message.set(response.error?.detail || 'Não foi possível publicar a avaliação.')
    });
  }

  private runAction(action: (id: number) => ReturnType<GamesService['toggleFavorite']>, success: string): void {
    const current = this.game();
    if (!current) return;
    if (!localStorage.getItem('spacegames_access')) { this.router.navigateByUrl('/login'); return; }
    action(current.id).subscribe({ next: () => this.message.set(success), error: (response: { error?: { detail?: string } }) => this.message.set(response.error?.detail || 'Não foi possível concluir a ação.') });
  }
}
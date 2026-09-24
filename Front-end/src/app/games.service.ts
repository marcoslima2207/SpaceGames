import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Game {
  id: number;
  titulo: string;
  descricao: string;
  preco: number | string;
  gratuito: boolean;
  destaque: boolean;
  imagem_url_publica?: string;
  imagem?: string;
  categoria?: number | null;
  categoria_nome?: string;
  desenvolvedor?: string;
  avaliacao?: number | string;
  ano_lancamento?: number;
  link_download?: string;
  arquivo_instalacao?: string;
}

export interface AccountSummary {
  user: { username: string; email: string; first_name: string; date_joined: string };
  favoritos: Game[];
  biblioteca: Game[];
  carrinho: { id: number; jogo: Game; quantidade: number; subtotal: number | string }[];
}

export interface Review {
  id: number;
  jogo: number;
  usuario_nome: string;
  nota: number;
  comentario: string;
  data_criacao: string;
}

@Injectable({ providedIn: 'root' })
export class GamesService {
  private readonly http = inject(HttpClient);

  getGames(): Observable<Game[]> {
    return this.http.get<Game[] | { results: Game[] }>('/api/jogos/').pipe(
      map((response) => Array.isArray(response) ? response : response.results)
    );
  }

  getAccountSummary(): Observable<AccountSummary> {
    const token = localStorage.getItem('spacegames_access') || '';
    return this.http.get<AccountSummary>('/api/auth/me/', {
      headers: new HttpHeaders({ Authorization: `Bearer ${token}` })
    });
  }

  toggleFavorite(gameId: number): Observable<unknown> {
    return this.http.post(`/api/jogos/${gameId}/favorito/`, {}, { headers: this.authHeaders() });
  }

  addToCart(gameId: number): Observable<unknown> {
    return this.http.post(`/api/jogos/${gameId}/carrinho/`, {}, { headers: this.authHeaders() });
  }

  addFreeGame(gameId: number): Observable<unknown> {
    return this.http.post(`/api/jogos/${gameId}/gratuito/`, {}, { headers: this.authHeaders() });
  }

  checkout(): Observable<unknown> {
    return this.http.post('/api/carrinho/finalizar/', {}, { headers: this.authHeaders() });
  }

  removeFromCart(itemId: number): Observable<unknown> {
    return this.http.delete(`/api/carrinho/${itemId}/`, { headers: this.authHeaders() });
  }

  getReviews(gameId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`/api/jogos/${gameId}/avaliacoes/`);
  }

  saveReview(gameId: number, nota: number, comentario: string): Observable<Review> {
    return this.http.post<Review>(`/api/jogos/${gameId}/avaliacoes/`, { nota, comentario }, { headers: this.authHeaders() });
  }

  private authHeaders(): HttpHeaders {
    return new HttpHeaders({ Authorization: `Bearer ${localStorage.getItem('spacegames_access') || ''}` });
  }
}
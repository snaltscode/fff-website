import crypto from 'node:crypto';
import { get, query, run } from './db';

// Session memory cache (matches Python SESSIONS dict)
interface SessionData {
  user: any;
  createdAt: number;
  lastVerified: number;
}

const SESSIONS: Map<string, SessionData> = (globalThis as any).__F4F_SESSIONS__ || ((globalThis as any).__F4F_SESSIONS__ = new Map<string, SessionData>());

export function hashPassword(password: string, salt?: string): string {
  const actualSalt = salt || crypto.randomBytes(16).toString('hex');
  const key = crypto.pbkdf2Sync(password, actualSalt, 100000, 32, 'sha256');
  return `${actualSalt}$${key.toString('hex')}`;
}

export function verifyPassword(storedPasswordHash: string, candidate: string): boolean {
  try {
    const [salt, storedKey] = storedPasswordHash.split('$');
    if (!salt || !storedKey) return false;
    const candidateKey = crypto.pbkdf2Sync(candidate, salt, 100000, 32, 'sha256').toString('hex');
    return crypto.timingSafeEqual(Buffer.from(storedKey, 'hex'), Buffer.from(candidateKey, 'hex'));
  } catch (error) {
    return false;
  }
}

export function generateOtp(): string {
  return (Math.floor(100000 + Math.random() * 900000)).toString();
}

export function hashOtp(otpStr: string): string {
  return crypto.createHash('sha256').update(otpStr).digest('hex');
}

export function createSessionToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

export function createSession(user: any): string {
  const token = createSessionToken();
  const userClean = { ...user };
  delete userClean.password_hash;
  const now = Date.now();
  SESSIONS.set(token, {
    user: userClean,
    createdAt: now,
    lastVerified: now,
  });
  return token;
}

export async function getAuthUser(authHeader?: string | null): Promise<any | null> {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null;
  }
  const token = authHeader.substring(7).trim();
  const session = SESSIONS.get(token);

  if (session) {
    const now = Date.now();
    // Cache validation within 30 seconds
    if (now - session.lastVerified < 30000) {
      return session.user;
    }

    // Refresh from database
    const dbUser = get('SELECT id, email, role, status, email_verified, avatar_url FROM users WHERE id = ?', [session.user.id]);
    if (dbUser) {
      session.user = { ...session.user, ...dbUser };
      session.lastVerified = now;
      return session.user;
    } else {
      SESSIONS.delete(token);
    }
  }

  return null;
}

export async function verifyGoogleIdToken(credential: string, clientId?: string): Promise<{ payload?: any; error?: string }> {
  try {
    const res = await fetch(`https://oauth2.googleapis.com/tokeninfo?id_token=${encodeURIComponent(credential)}`);
    if (!res.ok) {
      return { error: 'Invalid Google ID token.' };
    }
    const payload = await res.json();
    if (clientId && payload.aud && payload.aud !== clientId) {
      return { error: 'Google Client ID mismatch.' };
    }
    return { payload };
  } catch (err: any) {
    return { error: err.message || 'Failed to verify Google token.' };
  }
}

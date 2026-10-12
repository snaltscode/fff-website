export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { getAuthUser } from '@/lib/auth';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const body = await req.json();
    const dataUrl = body.image_data;
    if (!dataUrl || !dataUrl.includes('base64,')) {
      return NextResponse.json({ error: 'Valid Base64 image_data is required.' }, { status: 400 });
    }

    const parts = dataUrl.split('base64,');
    if (parts.length < 2 || !parts[1]) {
      return NextResponse.json({ error: 'Malformed base64 image data.' }, { status: 400 });
    }

    const mimeMatch = parts[0].match(/:(.*?);/);
    const mimeType = mimeMatch ? mimeMatch[1].toLowerCase() : '';
    
    const allowedMimes: Record<string, string> = {
      'image/jpeg': '.jpg',
      'image/jpg': '.jpg',
      'image/png': '.png',
      'image/webp': '.webp',
      'image/svg+xml': '.svg',
    };

    const ext = allowedMimes[mimeType];
    if (!ext) {
      return NextResponse.json({ error: 'Unsupported file type. Only JPEG, PNG, WebP, and SVG images are accepted.' }, { status: 400 });
    }

    const buffer = Buffer.from(parts[1], 'base64');
    if (buffer.length > 5 * 1024 * 1024) {
      return NextResponse.json({ error: 'File size exceeds maximum allowed limit of 5MB.' }, { status: 400 });
    }

    const filename = `${crypto.randomBytes(8).toString('hex')}_upload${ext}`;
    const uploadDir = path.resolve(process.cwd(), 'public', 'assets', 'uploads');

    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }

    const filePath = path.join(uploadDir, filename);
    fs.writeFileSync(filePath, buffer);

    return NextResponse.json({
      success: true,
      url: `/assets/uploads/${filename}`,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

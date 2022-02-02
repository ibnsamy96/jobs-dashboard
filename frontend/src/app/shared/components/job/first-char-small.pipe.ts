import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'firstCharSmall',
})
export class FirstCharSmallPipe implements PipeTransform {
  transform(value: string, ...args: unknown[]): string {
    const firstChar = value[0];
    const firstCharSmall = firstChar.toLocaleLowerCase();

    return firstCharSmall;
  }
}
